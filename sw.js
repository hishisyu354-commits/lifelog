// Lifelog Service Worker
// バージョンを上げるとキャッシュがリフレッシュされる
const CACHE_NAME = "lifelog-v57";
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png"
];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // 1つでも失敗しても他はキャッシュする
      return Promise.all(
        APP_SHELL.map((url) =>
          cache.add(url).catch((err) => console.warn("SW cache add failed:", url, err))
        )
      );
    })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);

  // Google API / GIS / Identity 系はキャッシュせず常にネット
  const noCacheHosts = [
    "googleapis.com",
    "google.com",
    "gstatic.com",
    "googleusercontent.com"
  ];
  if (noCacheHosts.some((h) => url.hostname.endsWith(h))) {
    return; // デフォルトの fetch を使わせる
  }

  // 同一オリジン：ネット優先、失敗時キャッシュ
  if (url.origin === self.location.origin) {
    event.respondWith(
      fetch(req)
        .then((resp) => {
          // 正常レスポンスだけ動的キャッシュ更新
          if (resp && resp.status === 200 && resp.type === "basic") {
            const clone = resp.clone();
            caches.open(CACHE_NAME).then((cache) => {
              try { cache.put(req, clone); } catch (e) {}
            });
          }
          return resp;
        })
        .catch(() => {
          // オフライン：キャッシュにあれば返す、なければルートを返す
          return caches.match(req).then((cached) => cached || caches.match("./"));
        })
    );
  }
});

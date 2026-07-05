if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(function(registrations) {
    for (let registration of registrations) {
      registration.unregister();
    }
  }).then(() => {
    window.location.reload(true);
  });
}
window.MSRTC_DATA = {
  announcements: [], news: [], popularRoutes: [], locations: [], depots: [], busTypes: [], buses: [], routes: [], tenders: [], recruitments: [], circulars: [], concessions: [], translations: { en: {}, mr: {}, hi: {} }, aboutData: { leadership: [] }
};

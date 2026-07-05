if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(function(registrations) {
    if (registrations.length > 0) {
      let unregisters = registrations.map(reg => reg.unregister());
      Promise.all(unregisters).then(() => {
        window.location.reload(true);
      });
    }
  });
}
window.MSRTC_DATA = {
  announcements: [], news: [], popularRoutes: [], locations: [], depots: [], busTypes: [], buses: [], routes: [], tenders: [], recruitments: [], circulars: [], concessions: [], translations: { en: {}, mr: {}, hi: {} }, aboutData: { leadership: [] }
};

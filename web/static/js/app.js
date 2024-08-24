const messageList = document.querySelectorAll(".message-item");

messageList.forEach((message) => {
  message.querySelector(".message-delete").addEventListener("click", () => {
    message.remove();
  });
});


mixpanel.init("9c037dcffbd1a460253aed19d1953cd5", {
  debug: true,
  track_pageview: true,
  persistence: "localStorage",
});

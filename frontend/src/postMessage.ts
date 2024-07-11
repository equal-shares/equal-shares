const MESSAGE_TYPE = {
  getHeight: 'getHeight',
  sendHeight: 'sendHeight',
  resised: 'resised',
};

function getDocumentHeight() {
  return Math.max(
    document.body.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.clientHeight,
    document.documentElement.scrollHeight,
    document.documentElement.offsetHeight,
  );
}

function onReceiveMessage(event: MessageEvent) {
  console.log('onReceiveMessage', event, getDocumentHeight());

  const payload = JSON.parse(event.data);

  if (event.source !== window.parent) {
    return;
  }

  if (event.source === window) {
    return;
  }

  if (!payload.type) {
    console.log("PostMessage: Missing 'type' in payload (event.data)", payload);
    return;
  }

  if (payload.type === MESSAGE_TYPE.getHeight) {
    event.source.postMessage(
      JSON.stringify({
        type: MESSAGE_TYPE.sendHeight,
        height: getDocumentHeight(),
      }),
    );
    return;
  }

  console.log('PostMessage: Unknown message type ', payload.type);
}

function onDocumentResize() {
  console.log('onDocumentResize', getDocumentHeight());

  window.parent.postMessage(
    JSON.stringify({
      type: MESSAGE_TYPE.resised,
      height: getDocumentHeight(),
    }),
    '*',
  );
}

export function registerPostMessage() {
  console.log('registerPostMessage');

  window.addEventListener('message', onReceiveMessage);
  window.addEventListener('resize', onDocumentResize);

  onDocumentResize();
}

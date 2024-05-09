import React from 'react';

const Toast = () => {
return (
    <div class="toast position-fixed bottom-0 end-50 p-3 text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="d-flex">
      <div class="toast-body">
        חריגה מיתרת הניקוד
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  </div>
);
};

export default Toast;

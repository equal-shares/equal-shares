<?php

/**
 * Vote Equal Shares Widget - Custom Elementor Widget
 *
 * Description: It display iframe of Equal Shares Vote page with email and token as query params
 */

 add_action('elementor/widgets/widgets_registered', 'vote_equal_shares_widgets_registered', 99);
 function vote_equal_shares_widgets_registered($widgets_manager) {
	 class VoteEqualSharesWidget extends \Elementor\Widget_Base {
		 public function get_name() {
			 return 'vote-equal-shares';
		 }

		 public function get_title() {
			 return 'vote-equal-shares';
		 }

		 public function get_icon() {
			 return 'eicon-code';
		 }

		 public function get_categories() {
			 return [ 'general', 'ariel-uni' ];
		 }

		 public function get_keywords() {
			 return [ 'vote-equal-shares' ];
		 }

		 protected function render() {
			 ?>
			 <iframe id="vote-equal-shares" src="<?php echo $this->_geIframetSrc(); ?>" width="100%" height="500px" frameborder="0" allowfullscreen></iframe>
			 <script>
				 const iframe = document.querySelector('#vote-equal-shares');

				 iframe.contentWindow.postMessage(JSON.stringify({
					 'type': 'getHeight'
				 }));

				 window.addEventListener('message', function(e) {
					 if (e.source !== iframe.contentWindow) {
						 return;
					 }

					 const data = JSON.parse(e.data);

					 if (typeof(data.type) !== 'string') {
						 return;
					 }

					 let iframeHeight = parseInt(iframe.getAttribute('height').replace('px', ''));
					 if (typeof(iframeHeight) !== 'number') {
						 iframeHeight = 1;
					 }

					 if (data.type === 'setHeight' || data.type === 'resised') {
						 if (iframeHeight != data.height) {
							 iframe.setAttribute('height', data.height + 'px');
						 }
					 }
				 });
			 </script>
			 <?php
		 }

		 private function _getPublicRSAKey() {
			 $key = "-----BEGIN PUBLIC KEY-----\r\n";
			 // Add here the Public RSA Key
			 $key .= "-----END PUBLIC KEY-----\r\n";
			 return $key;
		 }

		 private function _emailToToken($email) {
			 $public_key = openssl_pkey_get_public($this->_getPublicRSAKey());

			 $ok = openssl_public_encrypt($email, $encrypted, $public_key, OPENSSL_PKCS1_OAEP_PADDING);

			 if (!$ok) {
				 return '-';
			 }

			 return base64_encode($encrypted);
		 }

		 private function _geIframetSrc() {
			 $current_user = wp_get_current_user();
			 $email = $current_user->user_email;
			 $token = $this->_emailToToken($email);
			 return "https://arielcs.xyz/?email=" . urlencode($email) . '&token=' . urlencode($token);
		 }
	 }

	 $widgets_manager->register_widget_type(new \VoteEqualSharesWidget());
 }

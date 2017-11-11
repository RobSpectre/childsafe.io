/**
 * Icon's Demo.
 *
 * @author Htmlstream
 * @version 1.0
 * @requires chart.js (v1.0.3)
 *
 */
;(function($){
	'use strict';

  $('.u-icons-demo-item__value').each(function() {
    var IconsValue = $(this).siblings('.u-icon-v1').children().attr('class');
    $(this).val(IconsValue);
  });

})(jQuery);
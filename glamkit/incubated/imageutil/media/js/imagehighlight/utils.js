function generatePreviewFunc(identifier, preview_width, preview_height){
    preview_func = function(coords){
    	var rx = preview_width / coords.w;
    	var ry = preview_height / coords.h;
    	var image_width = $("#jcrop_target_" + identifier).width();
    	var image_height = $("#jcrop_target_" + identifier).height();
    	
    	$('#preview_' + identifier).css({
    		width: Math.round(rx * image_width) + 'px',
    		height: Math.round(ry * image_height) + 'px',
    		marginLeft: '-' + Math.round(rx * coords.x) + 'px',
    		marginTop: '-' + Math.round(ry * coords.y) + 'px'
    	});

    	$("#" + identifier + "_highlight_x").val(coords.x);
    	$("#" + identifier + "_highlight_y").val(coords.y);
    	$("#" + identifier + "_highlight_width").val(coords.w);
    	$("#" + identifier + "_highlight_height").val(coords.h);
    }
    return preview_func
}
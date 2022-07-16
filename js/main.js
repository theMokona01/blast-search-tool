function runSearch( term ) {
    $('#results').hide();
    $('#orf').empty();
    $('#blast').empty();
    var frmStr = $('#DNA_search').serialize();
    $.ajax({
        url: './blast.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert('FATAL ERROR IN DNA SEARCH (' + textStatus +
                  ') Error #: (' + errorThrown + ')');
        }
    });
}

function processJSON( data ) {
    $('#numORFs').text( data.numORFs );
    var next_row_num = 1;
    $.each( data.openReadingFrames, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
        $('<tr/>', { 'id' : this_row_id } ).appendTo('#orf');
        $('<td/>', { 'text' : item.orfID } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.geneStart } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.geneEnd } ).appendTo('#' + this_row_id);
    });
    $('#seqLength').text( data.seqLength ); 
    $('#numBlastAlignments').text( data.numBlastAlignments ); 
    $.each( data.blastResults, function(i, item) {
	var this_row_id = 'result_row_' + next_row_num++;
	$('<tr/>', { 'id' : this_row_id } ).appendTo('#blast');
	$('<td/>', { 'text' : item.blastID } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.blastScore } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.blastEVal } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.blastStrand } ).appendTo('#' + this_row_id);
        $('<td/>', { 'text' : item.blastPerIdn } ).appendTo('#' + this_row_id);
	$('<td/>', { 'text' : item.blastLength } ).appendTo('#' + this_row_id);
    }); 
    $('#results').show();
}

$(document).ready( function() {
	$('#submit').click( function() {
		runSearch(); 
		return false; 
	}); 
}); 

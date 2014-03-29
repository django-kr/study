/** @jsx React.DOM */

$(function(){
    $.ajax({
        url: '/jack/timeline/1',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            React.renderComponent(
                <p>{data[0].text}</p>,
                document.getElementById('example')
            );
        }
    });
});

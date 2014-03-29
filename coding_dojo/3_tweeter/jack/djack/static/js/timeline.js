/** @jsx React.DOM */

$(function(){
    var Post = React.createClass({
        render: function() {
            return (
            <div className="post">
                <h3>Tweet {this.props.data.id}</h3>
                <p>{this.props.data.text} posted by {this.props.data.writer_id}</p>
            </div>
            );
        }
    });

    $.ajax({
        url: '/jack/timeline/1', // XXX 1
        dataType: 'json',
        success: function(data) {
            var posts = data.map(function(post) {
                return <Post data={post}></Post>
            });
            React.renderComponent(
                <p>{posts}</p>,
                document.getElementById('example')
            );
        }
    });
});

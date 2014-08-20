<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1">
    <title>listrr</title>
    ${component.static_manager.render_static(component) | n}
</head>
<body>
    <h1>list&nbsp;<span class="strong">rr</span></h1>
    <span class="tagline">Simple, nested task list.</span>
    <section id="action">
        <form action="${request.route.find('api')}" method="POST">
            <input class="js_animated" style="display: none" placeholder="e.g. TODO Chores" type="text" name="title">
            <button id="main_button" disabled>Create List</button>
        </form>
    </section>
    <a style="position: absolute; bottom: 0" href="/u9zOeImsumoI5Dd_55EBnPR_">rootlink</a>
    <script>
        $(document).ready(function(){
            init_miniform($('form'), function(url){
                window.location = url;
            });
        });
    </script>
</body>
</html>

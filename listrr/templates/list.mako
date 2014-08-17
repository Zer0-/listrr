<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1">
    <title>listrr &mdash; ${head.title}</title>
    ${component.static_manager.render_static(component) | n}
</head>
<body>
    <header><a href="/">Home</a></header>
    <h1>${head.title}</h1>
    <ul>
        %for li in tree:
            <li>${li.title}</li>
        %endfor
        <li><button class="ico_action">+</button></li>
    </ul>
</body>
</html>

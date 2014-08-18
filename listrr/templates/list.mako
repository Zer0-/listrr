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
        <li>
            <form action="${request.route.find('new_list_item', (head.id,))}" method="POST" class="new_item_form">
                <input style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                <button class="ico_action" type="submit" disabled>+</button>
            </form>
        </li>
    </ul>
</body>
</html>

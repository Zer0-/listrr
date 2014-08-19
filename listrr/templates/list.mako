<%def name="rlist(tree, parent)">
    <ul>
        %for li in tree:
            <li>
                <div>${li.title}</div>
                %if li.replies:
                    ${rlist(li.replies, li)}
                %endif
            </li>
        %endfor
        <li>
            <form action="${request.route.find('new_list_item', (parent.id,))}" method="POST" class="new_item_form">
                <input style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                <button title="Add a list item" class="ico_action" type="submit" disabled>+</button>
                <button title="Cancel" class="ico_action" type="reset" style="display: none">&times;</button>
            </form>
        </li>
    </ul>
</%def>
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
    ${rlist(tree, head)}
    <div class="js-templates" style="display: none">
        <div data-js_template_name="list_item" data-js_template_fieldname="content" data-js_template_fieldtype="append"></div>
        <li data-js_template_name="li_form">
            <form data-js_template_fieldname="action" data-js_template_fieldtype="setattr" method="POST" class="new_item_form">
                <input style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                <button title="Add a list item" class="ico_action" type="submit" disabled>+</button>
                <button title="Cancel" class="ico_action" type="reset" style="display: none">&times;</button>
            </form>
        </li>
    </div>
</body>
</html>

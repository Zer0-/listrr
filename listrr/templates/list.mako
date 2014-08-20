<%def name="rlist(tree, parent)">
    <ul>
        %for li in tree:
            <li>
                <div>
                    <div class="rowitem title" title="Click to mark off">
                        ${li.title | h}
                    </div>
                    <div class="rowitem menu" title="Item menu">
                        <div class="menu_icon"></div>
                        <div class="menu_item dark"></div>
                        <div class="menu_item">
                            <form class="del_item_form" action="${request.route.find('api', (li.id,))}" method="DELETE">
                                <button type="submit" class="ico_action" title="delete list item">&times;</button>
                            </form>
                        </div>
                        <div class="menu_item">
                            <a class="ico_action" href="${request.route.find('list', (li.id,))}" title="Link to dedicated page">&#x2693;</a>
                        </div>
                        <div class="menu_item">
                            <form class="del_item_form" action="${request.route.find('api')}" method="DELETE">
                                <button type="submit" class="ico_action" title="Edit item text">✐</button>
                            </form>
                        </div>
                        <div class="menu_item">
                            <form class="del_item_form" action="${request.route.find('api')}" method="DELETE">
                                <button type="submit" class="ico_action" title="Revert to unmarked state">&#x25ef;</button>
                            </form>
                        </div>
                    </div>
                </div>
                %if li.replies:
                    ${rlist(li.replies, li)}
                %endif
            </li>
        %endfor
        <li>
            <form action="${request.route.find('api', (parent.id,))}" method="POST" class="new_item_form">
                <input class="js_animated" style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                <button title="Add a list item" class="ico_action" disabled>+</button>
                <button title="Cancel" class="ico_action js_animated" type="reset" style="display: none">&times;</button>
            </form>
        </li>
    </ul>
</%def>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1">
    <title>listrr &mdash; ${head.title[:30] | h}</title>
    ${component.static_manager.render_static(component) | n}
</head>
<body>
    <header><a href="/">Home</a></header>
    <h1>${head.title | h}</h1>
    ${rlist(tree, head)}
    <div class="js-templates" style="display: none">
        <div data-js_template_name="list_item" data-js_template_fieldname="content" data-js_template_fieldtype="append"></div>
        <li data-js_template_name="li_form">
            <form data-js_template_fieldname="action" data-js_template_fieldtype="setattr" method="POST" class="new_item_form">
                <input class="js_animated" style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                <button title="Add a list item" class="ico_action" disabled>+</button>
                <button title="Cancel" class="ico_action js_animated" type="reset" style="display: none">&#x2716;</button>
            </form>
        </li>
    </div>
    <footer></footer>
</body>
</html>

<%def name="rlist(tree, parent)">
    <ul>
        %for li in tree:
            <%
                api_url = request.route.find('api', (li.id,))
                item_url = request.route.find('list', (li.id,))
                done = 'done' if li.done else ''
                leaf = '' if li.replies else 'leaf'
            %>
            <li id="${li.id}" data-item_url="${item_url}" data-api_url="${api_url}" class="${done} ${leaf}">
                <div class="item_body">
                    <div class="rowitem title">
                        ${li.title | h}
                    </div>
                    <button title="Click to mark off" class="ico_action rowitem btn_mark">✓</button>
                    <div class="rowitem menu" title="Item menu">
                        <div class="menu_icon"></div>
                    </div>
                    <div class="rowitem spacer"></div>
                </div>
                %if li.replies:
                    ${rlist(li.replies, li)}
                %endif
            </li>
        %endfor
        <li class="new_form_container">
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
    <main>
        ${rlist(tree, head)}
    </main>
    <div class="js-templates" style="display: none">
        <li
        data-js_template_name="list_item"
        data-js_template_fieldtype='setattr, setattr, setattr'
        data-js_template_fieldname='id, data-item_url, data-api_url'
        class="leaf">
            <div class="item_body">
                <div class="rowitem title" data-js_template_fieldtype='append' data-js_template_fieldname='title'></div>
                <button title="Click to mark off" class="ico_action rowitem btn_mark">✓</button>
                <div class="rowitem menu" title="Item menu">
                    <div class="menu_icon"></div>
                </div>
                <div class="rowitem spacer"></div>
            </div>
        </li>
        <ul data-js_template_name="list">
            <li class="new_form_container">
                <form data-js_template_fieldname="action" data-js_template_fieldtype="setattr" method="POST" class="new_item_form">
                    <input class="js_animated" style="display: none" placeholder="e.g. Mop Floors" type="text" name="title">
                    <button title="Add a list item" class="ico_action" disabled>+</button>
                    <button title="Cancel" class="ico_action js_animated" type="reset" style="display: none">&times;</button>
                </form>
            </li>
        </ul>
        <div data-js_template_name="menu_buttons" class="menu_items">
            <div class="menu_item dark"></div>
            <div class="menu_item">
                <button class="ico_action delete" title="delete list item">&times;</button>
            </div>
            <div class="menu_item">
                <a class="ico_action" data-js_template_fieldtype="setattr" data-js_template_fieldname="href" title="Link to dedicated page">&#x2693;</a>
            </div>
            <div class="menu_item" data-js_template_fieldname="sublist" data-js_template_fieldtype="toggle">
                <button class="ico_action sublist" title="Add a sub-list to this item">+</button>
            </div>
            <div class="menu_item">
                <button class="ico_action" title="Edit item text">✐</button>
            </div>
            <div class="menu_item" data-js_template_fieldname="unmark" data-js_template_fieldtype="toggle">
                <button class="ico_action unmark" title="Revert to unmarked state">&#x25ef;</button>
            </div>
        </div>
    </div>
    <footer></footer>
</body>
</html>

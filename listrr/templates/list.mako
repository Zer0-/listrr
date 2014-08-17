<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <h1>${head.title}</h1>
    <ul>
        %for li in tree:
            <li>${li.title}</li>
        %endfor
    </ul>
</body>
</html>

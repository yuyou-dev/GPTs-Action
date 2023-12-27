<?php
$redis = new Redis();
// 设置响应头为 JSON 格式
header('Content-Type: application/json');

// 确保$_GET参数存在
$value = isset($_GET['value']) ? intval($_GET['value']) : 0;
$color = isset($_GET['color']) ? $_GET['color'] : 'default';

// 存入redis
$redis->hMSet("gpt-data", array(
    "light_on" => 1,
    "light_value" => $value,
    "color" => $color
));

// 构建要返回的关联数组
$response = array(
    "response" => "已经开灯",
    "value" => $value,
    "color" => $color
);

// 直接输出JSON数据
echo json_encode($response, JSON_UNESCAPED_UNICODE);
?>

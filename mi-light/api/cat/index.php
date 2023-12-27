<?php
$redis = new Redis();
// 设置响应头为 JSON 格式
header('Content-Type: application/json');

$number = intval($_GET['number']);
// 输入食物的数量
$redis->hSet("gpt-data", "number", $number);
// 增加一个变量，防止重复喂食
$redis->hIncrBy("gpt-data", "index", 1);


// 构建要返回的关联数组
$response = array(
    "response" => "已经出食物",
    "number" => $number,
);

// 将关联数组转换为 JSON 格式
$json_response = json_encode($response, JSON_UNESCAPED_UNICODE);

// 输出 JSON 数据
echo $json_response;
?>
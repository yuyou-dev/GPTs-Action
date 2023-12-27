<?php
$redis = new Redis();
// 设置响应头为 JSON 格式
header('Content-Type: application/json');
$redis->hSet("gpt-data", "light_on", 2);

// 构建要返回的关联数组
$response = array(
    "response" => "已经关灯",
);
// 将关联数组转换为 JSON 格式
$json_response = json_encode($response, JSON_UNESCAPED_UNICODE);
// 输出 JSON 数据
echo $json_response;
?>

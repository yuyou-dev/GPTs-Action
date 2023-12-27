<?php
$redis = new Redis();
// 设置响应头为 JSON 格式
header('Content-Type: application/json');

// 获取 "number" 的值
$number = $redis->hGet("gpt-data", "number");
$index = $redis->hGet("gpt-data", "index");

// 返回JSON格式的响应包含两个值
echo json_encode(['number' => $number, 'index' => $index]);
?>

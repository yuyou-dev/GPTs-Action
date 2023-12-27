<?php
$redis = new Redis();
// 设置响应头为 JSON 格式
header('Content-Type: application/json');

// 获取 "light_on" 的值
$lightOn = $redis->hGet("gpt-data", "light_on");
// 获取 "light_value" 的值
$lightValue = $redis->hGet("gpt-data", "light_value");
$color = $redis->hGet("gpt-data", "color");

// 返回JSON格式的响应包含两个值
echo json_encode(['light_on' => $lightOn, 'light_value' => $lightValue, 'color' => $color]);
?>

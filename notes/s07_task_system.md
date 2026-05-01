# Task System

## 任务图

1. CRUD + 依赖图
2. task_create & task_update & task_list & task_get

## 解决的问题

1. 什么可以做？ → status=pending 且 blockedBy=[] 的任务
2. 什么被卡住？ → 还在等前置完成的任务
3. 什么做完了？ → completed 的任务，完成时自动从其他任务的 blockedBy 中移除自己，从而解锁后续
CREATE DATABASE IF NOT EXISTS hrm CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS hrm_flowable CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE hrm;
SOURCE /seed/hrm.sql;
SOURCE /seed/demo.sql;

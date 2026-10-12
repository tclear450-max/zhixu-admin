-- Applied ONLY when the delivery MySQL volume is first initialized.
USE hrm;
UPDATE sys_staff SET name=CONCAT('演示员工',LPAD(id,2,'0')),pwd='$2b$12$5Jf2.EjUqP1SsIxmlB2T..HnJaBFQOj0SboKyRari0McrlktFmzLu',avatar='',phone=NULL,address='演示园区',birthday='1995-01-01',remark='知序人事演示数据';
UPDATE sys_staff SET name='知序管理员',dept_id=12 WHERE id=1;
UPDATE sys_staff SET name='林知 · 人事',dept_id=17,status=1 WHERE id=9;
UPDATE sys_staff SET name='周序 · 主管',dept_id=12,status=1 WHERE id=2;
UPDATE sys_staff SET name='陈晨 · 员工',dept_id=12,status=1 WHERE id=3;
UPDATE sys_dept SET mor_start_time='09:00:00',mor_end_time='12:00:00',aft_start_time='13:00:00',aft_end_time='18:00:00',total_work_time=8.0 WHERE parent_id<>0;
UPDATE sys_dept SET name='产品研发一组' WHERE id=12;
UPDATE sys_dept SET name='产品研发二组' WHERE id=13;
UPDATE sys_dept SET name='产品研发中心' WHERE id=11;
DELETE FROM att_staff_leave;
DELETE FROM att_staff_overtime;
DELETE FROM att_attendance;
DELETE FROM sys_docs;
DELETE FROM sal_salary;
DELETE FROM att_leave;
INSERT INTO att_leave (dept_id,days,type_num,status,remark)
SELECT id,10,0,1,'演示事假额度' FROM sys_dept WHERE parent_id<>0;
INSERT INTO att_leave (dept_id,days,type_num,status,remark)
SELECT id,10,2,1,'演示病假额度' FROM sys_dept WHERE parent_id<>0;
INSERT INTO sal_salary (staff_id,base_salary,day_salary,hour_salary,subsidy,bonus,total_salary,month,remark)
SELECT id,8000+id*100,ROUND((8000+id*100)/21.75,3),ROUND((8000+id*100)/174,3),300,500,8800+id*100,DATE_FORMAT(CURDATE(),'%Y%m'),'演示预置金额，非正式薪资结果' FROM sys_staff WHERE status=1;
INSERT INTO att_attendance (staff_id,mor_start_time,mor_end_time,aft_start_time,aft_end_time,attendance_date,status,remark)
SELECT s.id,IF(MOD(s.id+d.n,9)=0,'09:15:00','09:00:00'),'12:00:00','13:00:00','18:00:00',DATE_SUB(CURDATE(),INTERVAL d.n DAY),IF(MOD(s.id+d.n,9)=0,1,0),'演示考勤'
FROM sys_staff s CROSS JOIN (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14) d
WHERE s.status=1 AND WEEKDAY(DATE_SUB(CURDATE(),INTERVAL d.n DAY))<5;

CREATE TABLE IF NOT EXISTS zhixu_delivery_meta (id INT PRIMARY KEY, version VARCHAR(20));
INSERT INTO zhixu_delivery_meta VALUES (1,'1.0.0') ON DUPLICATE KEY UPDATE version='1.0.0';

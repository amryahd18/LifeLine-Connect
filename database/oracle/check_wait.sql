ALTER SESSION SET CONTAINER = XEPDB1;
SET LINESIZE 200;
COL event FORMAT A30;
COL state FORMAT A15;
SELECT sid, serial#, event, state, seconds_in_wait, blocking_session 
FROM v$session 
WHERE username = 'LIFELINE_USER';
EXIT;

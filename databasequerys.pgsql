-- create tablespace ts_primary in project directory
-- CREATE TABLESPACE ts_primary
--   OWNER postgres
--   LOCATION E'/home/aniket-yadav/WORKSPACE/WebProjects/.visenv/Visualizer';

-- ALTER TABLESPACE ts_primary
--   OWNER TO postgres;

-- GRANT CREATE ON TABLESPACE ts_primary TO root WITH GRANT OPTION;

-- -- CREATE database ICPC_Database

-- CREATE DATABASE "ICPC_Database"
--   WITH OWNER = root
--       ENCODING = 'UTF8'
--       TABLESPACE = ts_primary
--       CONNECTION LIMIT = -1;

SELECT * FROM public."visualCancer_breastcancerdata";

-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: masterscheduler
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schoolId` varchar(20) DEFAULT NULL,
  `grade_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_grade_school` (`schoolId`),
  CONSTRAINT `fk_grade_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `optionblock`
--

DROP TABLE IF EXISTS `optionblock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `optionblock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gradeId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_optionblock_grade` (`gradeId`),
  CONSTRAINT `fk_optionblock_grade` FOREIGN KEY (`gradeId`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `optiongroup`
--

DROP TABLE IF EXISTS `optiongroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `optiongroup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `optionBlockId` int DEFAULT NULL,
  `subjectId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_optiongroup_block` (`optionBlockId`),
  KEY `fk_optiongroup_subject` (`subjectId`),
  CONSTRAINT `fk_optiongroup_block` FOREIGN KEY (`optionBlockId`) REFERENCES `optionblock` (`id`),
  CONSTRAINT `fk_optiongroup_subject` FOREIGN KEY (`subjectId`) REFERENCES `subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `period`
--

DROP TABLE IF EXISTS `period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `period` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schoolId` varchar(20) DEFAULT NULL,
  `startTime` time DEFAULT NULL,
  `endTime` time DEFAULT NULL,
  `label` varchar(20) DEFAULT NULL,
  `isTeachingPeriod` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_period_school` (`schoolId`),
  CONSTRAINT `fk_period_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schoolId` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_resources_school` (`schoolId`),
  CONSTRAINT `fk_resources_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools` (
  `id` varchar(20) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `contact_name` varchar(50) DEFAULT NULL,
  `primary_contact` varchar(50) DEFAULT NULL,
  `primary_role` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `streams`
--

DROP TABLE IF EXISTS `streams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `streams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gradeId` int DEFAULT NULL,
  `streamName` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_streams_grade` (`gradeId`),
  CONSTRAINT `fk_streams_grade` FOREIGN KEY (`gradeId`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subjectrequirement`
--

DROP TABLE IF EXISTS `subjectrequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjectrequirement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schoolId` varchar(20) DEFAULT NULL,
  `subjectId` int DEFAULT NULL,
  `gradeId` int DEFAULT NULL,
  `lessonsPerWeek` int DEFAULT NULL,
  `doublesPerWeek` int DEFAULT NULL,
  `maxLessonsPerDay` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_subjectrequirement_school` (`schoolId`),
  KEY `fk_subjectrequirement_subject` (`subjectId`),
  KEY `fk_subjectrequirement_grade` (`gradeId`),
  CONSTRAINT `fk_subjectrequirement_grade` FOREIGN KEY (`gradeId`) REFERENCES `grade` (`id`),
  CONSTRAINT `fk_subjectrequirement_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`),
  CONSTRAINT `fk_subjectrequirement_subject` FOREIGN KEY (`subjectId`) REFERENCES `subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `schoolId` varchar(20) DEFAULT NULL,
  `requiresResourceId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_subjects_school` (`schoolId`),
  KEY `fk_subjects_resource` (`requiresResourceId`),
  CONSTRAINT `fk_subjects_resource` FOREIGN KEY (`requiresResourceId`) REFERENCES `resources` (`id`),
  CONSTRAINT `fk_subjects_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teacherassignment`
--

DROP TABLE IF EXISTS `teacherassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacherassignment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacherId` int DEFAULT NULL,
  `subjectId` int DEFAULT NULL,
  `streamId` int DEFAULT NULL,
  `optionGroupId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teacherassignment_teacher` (`teacherId`),
  KEY `fk_teacherassignment_subject` (`subjectId`),
  KEY `fk_teacherassignment_stream` (`streamId`),
  KEY `fk_teacherassignment_optiongroup` (`optionGroupId`),
  CONSTRAINT `fk_teacherassignment_optiongroup` FOREIGN KEY (`optionGroupId`) REFERENCES `optiongroup` (`id`),
  CONSTRAINT `fk_teacherassignment_stream` FOREIGN KEY (`streamId`) REFERENCES `streams` (`id`),
  CONSTRAINT `fk_teacherassignment_subject` FOREIGN KEY (`subjectId`) REFERENCES `subjects` (`id`),
  CONSTRAINT `fk_teacherassignment_teacher` FOREIGN KEY (`teacherId`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=192 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teacherconstraint`
--

DROP TABLE IF EXISTS `teacherconstraint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacherconstraint` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacherId` int DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `parameters` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teacherconstraint_teacher` (`teacherId`),
  CONSTRAINT `fk_teacherconstraint_teacher` FOREIGN KEY (`teacherId`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `phonenumber` int DEFAULT NULL,
  `schoolId` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teachers_school` (`schoolId`),
  CONSTRAINT `fk_teachers_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schoolId` varchar(20) DEFAULT NULL,
  `academic_year` int DEFAULT NULL,
  `term_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_term_school` (`schoolId`),
  CONSTRAINT `fk_term_school` FOREIGN KEY (`schoolId`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timetableentry`
--

DROP TABLE IF EXISTS `timetableentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetableentry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `termId` int DEFAULT NULL,
  `day` varchar(10) DEFAULT NULL,
  `subjectId` int DEFAULT NULL,
  `teacherId` int DEFAULT NULL,
  `periodId` int DEFAULT NULL,
  `doubleGroupId` int DEFAULT NULL,
  `streamId` int DEFAULT NULL,
  `optionGroupId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_timetableentry_term` (`termId`),
  KEY `fk_timetableentry_subject` (`subjectId`),
  KEY `fk_timetableentry_teacher` (`teacherId`),
  KEY `fk_timetableentry_period` (`periodId`),
  KEY `fk_timetableentry_stream` (`streamId`),
  KEY `fk_timetableentry_optiongroup` (`optionGroupId`),
  CONSTRAINT `fk_timetableentry_optiongroup` FOREIGN KEY (`optionGroupId`) REFERENCES `optiongroup` (`id`),
  CONSTRAINT `fk_timetableentry_period` FOREIGN KEY (`periodId`) REFERENCES `period` (`id`),
  CONSTRAINT `fk_timetableentry_stream` FOREIGN KEY (`streamId`) REFERENCES `streams` (`id`),
  CONSTRAINT `fk_timetableentry_subject` FOREIGN KEY (`subjectId`) REFERENCES `subjects` (`id`),
  CONSTRAINT `fk_timetableentry_teacher` FOREIGN KEY (`teacherId`) REFERENCES `teachers` (`id`),
  CONSTRAINT `fk_timetableentry_term` FOREIGN KEY (`termId`) REFERENCES `term` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-05 13:05:54

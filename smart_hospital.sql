CREATE DATABASE  IF NOT EXISTS `smart_hospital` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `smart_hospital`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: smart_hospital
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `dept_id` int DEFAULT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `reason` text,
  `status` enum('Scheduled','Completed','Cancelled','No Show') DEFAULT 'Scheduled',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointment_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `dept_id` (`dept_id`),
  KEY `idx_appointment_date` (`appointment_date`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bed_allocations`
--

DROP TABLE IF EXISTS `bed_allocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bed_allocations` (
  `allocation_id` int NOT NULL AUTO_INCREMENT,
  `bed_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `allocation_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `discharge_date` datetime DEFAULT NULL,
  `total_days` int DEFAULT NULL,
  `status` enum('Active','Completed') DEFAULT 'Active',
  PRIMARY KEY (`allocation_id`),
  KEY `bed_id` (`bed_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `bed_allocations_ibfk_1` FOREIGN KEY (`bed_id`) REFERENCES `beds` (`bed_id`) ON DELETE CASCADE,
  CONSTRAINT `bed_allocations_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bed_allocations`
--

LOCK TABLES `bed_allocations` WRITE;
/*!40000 ALTER TABLE `bed_allocations` DISABLE KEYS */;
/*!40000 ALTER TABLE `bed_allocations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beds`
--

DROP TABLE IF EXISTS `beds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beds` (
  `bed_id` int NOT NULL AUTO_INCREMENT,
  `bed_number` varchar(20) NOT NULL,
  `dept_id` int DEFAULT NULL,
  `ward_type` enum('ICU','General','Private','Emergency') NOT NULL,
  `bed_status` enum('Available','Occupied','Reserved','Under Maintenance') DEFAULT 'Available',
  `rate_per_day` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`bed_id`),
  UNIQUE KEY `bed_number` (`bed_number`),
  KEY `dept_id` (`dept_id`),
  KEY `idx_bed_status` (`bed_status`),
  CONSTRAINT `beds_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beds`
--

LOCK TABLES `beds` WRITE;
/*!40000 ALTER TABLE `beds` DISABLE KEYS */;
INSERT INTO `beds` VALUES (1,'ICU-001',6,'ICU','Available',5000.00,'2025-10-14 17:30:32'),(2,'ICU-002',6,'ICU','Available',5000.00,'2025-10-14 17:30:32'),(3,'ICU-003',6,'ICU','Available',5000.00,'2025-10-14 17:30:32'),(4,'GEN-001',5,'General','Available',2000.00,'2025-10-14 17:30:32'),(5,'GEN-002',5,'General','Available',2000.00,'2025-10-14 17:30:32'),(6,'PVT-001',1,'Private','Available',3500.00,'2025-10-14 17:30:32'),(7,'PVT-002',2,'Private','Available',3500.00,'2025-10-14 17:30:32'),(8,'EMG-001',6,'Emergency','Available',1500.00,'2025-10-14 17:30:32');
/*!40000 ALTER TABLE `beds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_details`
--

DROP TABLE IF EXISTS `bill_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_details` (
  `detail_id` int NOT NULL AUTO_INCREMENT,
  `bill_id` int NOT NULL,
  `item_type` enum('Room','Consultation','Lab Test','Medicine','Surgery','Nursing','Other') NOT NULL,
  `item_description` varchar(300) DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `rate` decimal(10,2) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`detail_id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `bill_details_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `billing` (`bill_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_details`
--

LOCK TABLES `bill_details` WRITE;
/*!40000 ALTER TABLE `bill_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `admission_id` int DEFAULT NULL,
  `bill_date` date NOT NULL,
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `insurance_claim_amount` decimal(12,2) DEFAULT '0.00',
  `discount_amount` decimal(12,2) DEFAULT '0.00',
  `tax_amount` decimal(10,2) DEFAULT '0.00',
  `net_amount` decimal(12,2) NOT NULL,
  `payment_status` enum('Pending','Partial','Paid','Refunded') DEFAULT 'Pending',
  `payment_method` enum('Cash','Card','UPI','Net Banking','Insurance') DEFAULT 'Cash',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`bill_id`),
  KEY `patient_id` (`patient_id`),
  KEY `idx_billing_date` (`bill_date`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing`
--

LOCK TABLES `billing` WRITE;
/*!40000 ALTER TABLE `billing` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `dept_id` int NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(100) NOT NULL,
  `floor_number` int DEFAULT NULL,
  `head_doctor_id` int DEFAULT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`dept_id`),
  UNIQUE KEY `dept_name` (`dept_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Cardiology',3,NULL,'0135-2745001','2025-10-14 17:30:32'),(2,'Neurology',4,NULL,'0135-2745002','2025-10-14 17:30:32'),(3,'Orthopedics',2,NULL,'0135-2745003','2025-10-14 17:30:32'),(4,'Pediatrics',1,NULL,'0135-2745004','2025-10-14 17:30:32'),(5,'General Medicine',1,NULL,'0135-2745005','2025-10-14 17:30:32'),(6,'Emergency',0,NULL,'0135-2745000','2025-10-14 17:30:32');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `doctor_performance`
--

DROP TABLE IF EXISTS `doctor_performance`;
/*!50001 DROP VIEW IF EXISTS `doctor_performance`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `doctor_performance` AS SELECT 
 1 AS `doctor_id`,
 1 AS `doctor_name`,
 1 AS `specialization`,
 1 AS `dept_name`,
 1 AS `total_appointments`,
 1 AS `total_prescriptions`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `doctor_schedule`
--

DROP TABLE IF EXISTS `doctor_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `schedule_date` date NOT NULL,
  `shift` enum('Morning','Evening','Night') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `status` enum('Scheduled','Completed','Cancelled') DEFAULT 'Scheduled',
  `max_patients` int DEFAULT '20',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`schedule_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `doctor_schedule_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_schedule`
--

LOCK TABLES `doctor_schedule` WRITE;
/*!40000 ALTER TABLE `doctor_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctor_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `dept_id` int DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `license_number` varchar(50) DEFAULT NULL,
  `years_of_experience` int DEFAULT NULL,
  `status` enum('Available','In Surgery','On Call','On Leave') DEFAULT 'Available',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `license_number` (`license_number`),
  KEY `idx_doctor_dept` (`dept_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'Rajesh','Kumar','Cardiologist',1,'9876543210','rajesh.kumar@hospital.com','DMC12345',15,'Available','2025-10-14 17:30:32'),(2,'Priya','Sharma','Neurologist',2,'9876543211','priya.sharma@hospital.com','DMC12346',12,'Available','2025-10-14 17:30:32'),(3,'Amit','Verma','Orthopedic Surgeon',3,'9876543212','amit.verma@hospital.com','DMC12347',10,'Available','2025-10-14 17:30:32'),(4,'Sneha','Patel','Pediatrician',4,'9876543213','sneha.patel@hospital.com','DMC12348',8,'Available','2025-10-14 17:30:32'),(5,'Arjun','Singh','General Physician',5,'9876543214','arjun.singh@hospital.com','DMC12349',20,'Available','2025-10-14 17:30:32');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergency_records`
--

DROP TABLE IF EXISTS `emergency_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency_records` (
  `emergency_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `patient_name` varchar(100) NOT NULL,
  `age` int DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `condition_description` text NOT NULL,
  `triage_level` enum('Critical','Urgent','Moderate','Low') NOT NULL,
  `arrival_time` datetime NOT NULL,
  `ambulance_used` tinyint(1) DEFAULT '0',
  `attending_doctor_id` int DEFAULT NULL,
  `status` enum('Waiting','In Treatment','Surgery','Stabilizing','Admitted','Discharged','Deceased') DEFAULT 'Waiting',
  `response_time_minutes` int DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`emergency_id`),
  KEY `patient_id` (`patient_id`),
  KEY `attending_doctor_id` (`attending_doctor_id`),
  KEY `idx_emergency_triage` (`triage_level`),
  CONSTRAINT `emergency_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE SET NULL,
  CONSTRAINT `emergency_records_ibfk_2` FOREIGN KEY (`attending_doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergency_records`
--

LOCK TABLES `emergency_records` WRITE;
/*!40000 ALTER TABLE `emergency_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergency_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurance`
--

DROP TABLE IF EXISTS `insurance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurance` (
  `insurance_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `provider_name` varchar(200) NOT NULL,
  `policy_number` varchar(100) NOT NULL,
  `coverage_amount` decimal(12,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('Active','Expired','Cancelled') DEFAULT 'Active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`insurance_id`),
  UNIQUE KEY `policy_number` (`policy_number`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `insurance_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurance`
--

LOCK TABLES `insurance` WRITE;
/*!40000 ALTER TABLE `insurance` DISABLE KEYS */;
/*!40000 ALTER TABLE `insurance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_tests`
--

DROP TABLE IF EXISTS `lab_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lab_tests` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int DEFAULT NULL,
  `test_name` varchar(200) NOT NULL,
  `test_type` varchar(100) DEFAULT NULL,
  `test_date` date NOT NULL,
  `result_date` date DEFAULT NULL,
  `status` enum('Pending','In Progress','Completed','Cancelled') DEFAULT 'Pending',
  `result_value` text,
  `normal_range` varchar(100) DEFAULT NULL,
  `remarks` text,
  `cost` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`test_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `lab_tests_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `lab_tests_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_tests`
--

LOCK TABLES `lab_tests` WRITE;
/*!40000 ALTER TABLE `lab_tests` DISABLE KEYS */;
/*!40000 ALTER TABLE `lab_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_history`
--

DROP TABLE IF EXISTS `medical_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_history` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `allergies` text,
  `chronic_conditions` text,
  `past_surgeries` text,
  `family_history` text,
  `current_medications` text,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`history_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `medical_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_history`
--

LOCK TABLES `medical_history` WRITE;
/*!40000 ALTER TABLE `medical_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `medical_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicines`
--

DROP TABLE IF EXISTS `medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicines` (
  `medicine_id` int NOT NULL AUTO_INCREMENT,
  `medicine_name` varchar(200) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `manufacturer` varchar(200) DEFAULT NULL,
  `description` text,
  `unit_of_measure` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`medicine_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicines`
--

LOCK TABLES `medicines` WRITE;
/*!40000 ALTER TABLE `medicines` DISABLE KEYS */;
INSERT INTO `medicines` VALUES (1,'Paracetamol 500mg','Painkiller','Cipla',NULL,'Tablets','2025-10-14 17:30:32'),(2,'Amoxicillin 250mg','Antibiotic','Sun Pharma',NULL,'Capsules','2025-10-14 17:30:32'),(3,'Ibuprofen 400mg','Painkiller','Ranbaxy',NULL,'Tablets','2025-10-14 17:30:32'),(4,'Metformin 500mg','Diabetes','Dr. Reddy',NULL,'Tablets','2025-10-14 17:30:32'),(5,'Aspirin 75mg','Blood Thinner','Bayer',NULL,'Tablets','2025-10-14 17:30:32'),(6,'Omeprazole 20mg','Antacid','Zydus',NULL,'Capsules','2025-10-14 17:30:32'),(7,'Ciprofloxacin 500mg','Antibiotic','Lupin',NULL,'Tablets','2025-10-14 17:30:32'),(8,'Insulin Glargine','Diabetes','Novo Nordisk',NULL,'Injection','2025-10-14 17:30:32');
/*!40000 ALTER TABLE `medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `patient_summary`
--

DROP TABLE IF EXISTS `patient_summary`;
/*!50001 DROP VIEW IF EXISTS `patient_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `patient_summary` AS SELECT 
 1 AS `patient_id`,
 1 AS `patient_name`,
 1 AS `date_of_birth`,
 1 AS `age`,
 1 AS `gender`,
 1 AS `blood_group`,
 1 AS `admission_type`,
 1 AS `status`,
 1 AS `bed_id`,
 1 AS `bed_number`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text,
  `emergency_contact_name` varchar(100) DEFAULT NULL,
  `emergency_contact_number` varchar(15) DEFAULT NULL,
  `admission_type` enum('OPD','IPD','Emergency') DEFAULT 'OPD',
  `admission_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `discharge_date` datetime DEFAULT NULL,
  `status` enum('Active','Discharged','Deceased') DEFAULT 'Active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`),
  KEY `idx_patient_name` (`first_name`,`last_name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'Vedika','Yadav','2003-05-15','Female','O+','9876000001',NULL,'Dehradun, Uttarakhand',NULL,NULL,'IPD','2025-10-14 23:00:32',NULL,'Active','2025-10-14 17:30:32'),(2,'Rahul','Mehta','1978-03-22','Male','A+','9876000002',NULL,'Mussoorie, Uttarakhand',NULL,NULL,'Emergency','2025-10-14 23:00:32',NULL,'Active','2025-10-14 17:30:32'),(3,'Anjali','Gupta','1992-08-10','Female','B+','9876000003',NULL,'Rishikesh, Uttarakhand',NULL,NULL,'OPD','2025-10-14 23:00:32',NULL,'Active','2025-10-14 17:30:32'),(4,'Vikram','Shah','1957-12-05','Male','AB-','9876000004',NULL,'Haridwar, Uttarakhand',NULL,NULL,'Emergency','2025-10-14 23:00:32',NULL,'Active','2025-10-14 17:30:32'),(5,'Pooja','Desai','1995-06-18','Female','O-','9876000005',NULL,'Dehradun, Uttarakhand',NULL,NULL,'IPD','2025-10-14 23:00:32',NULL,'Active','2025-10-14 17:30:32'),(6,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2025-10-15 20:28:28',NULL,'Active','2025-10-15 14:58:28'),(7,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2025-10-16 08:26:10',NULL,'Active','2025-10-16 02:56:10'),(8,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2025-11-16 18:04:24',NULL,'Active','2025-11-16 12:34:24'),(9,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2025-11-16 20:58:13',NULL,'Active','2025-11-16 15:28:13'),(10,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2025-11-17 10:03:56',NULL,'Active','2025-11-17 04:33:56'),(11,'gigi','hadid','2025-11-17','Female','A+','768997','yfyuk@gmail.com','kuerhfkishfl.oj','hgjjnki','1268409437','OPD','2025-11-17 11:19:51',NULL,'Active','2025-11-17 05:49:51'),(12,'bela','hadid','2025-11-17','Female','A+','768997675','hgcfck@gmail.com','ijiosuiofhugvh','gghhjhbg','1268409437','OPD','2025-11-17 11:20:38',NULL,'Active','2025-11-17 05:50:38'),(13,'kunal','singh','2025-11-17','Male','A+','35646476','kunal@gmail.com','ygkyutgkuki','ghjg','67576575','Emergency','2025-11-17 11:25:21',NULL,'Active','2025-11-17 05:55:21'),(15,'Miva','Test','2005-11-12','Female','O+','9876543210','miva@test.com','Test Address','John Doe','9123456789','IPD','2025-11-17 11:00:00','2025-11-17 15:00:00','Discharged','2025-11-17 08:00:05'),(16,'Test','Patient','1990-01-01','Male','B+','9999999999','test@hospital.com','Test Address','Emergency Contact','8888888888','OPD','2026-07-01 22:32:25',NULL,'Active','2026-07-01 17:02:25');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacy_inventory`
--

DROP TABLE IF EXISTS `pharmacy_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacy_inventory` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `medicine_id` int NOT NULL,
  `batch_number` varchar(50) DEFAULT NULL,
  `stock_quantity` int NOT NULL DEFAULT '0',
  `min_stock_level` int DEFAULT '50',
  `unit_price` decimal(10,2) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `supplier_name` varchar(200) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`),
  KEY `medicine_id` (`medicine_id`),
  KEY `idx_medicine_stock` (`stock_quantity`),
  CONSTRAINT `pharmacy_inventory_ibfk_1` FOREIGN KEY (`medicine_id`) REFERENCES `medicines` (`medicine_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacy_inventory`
--

LOCK TABLES `pharmacy_inventory` WRITE;
/*!40000 ALTER TABLE `pharmacy_inventory` DISABLE KEYS */;
INSERT INTO `pharmacy_inventory` VALUES (1,1,'PCM2024A',45,50,5.00,'2025-12-31','MediSupply Co','2025-10-14 17:30:32'),(2,2,'AMX2024B',120,100,15.00,'2025-08-15','PharmaDist Ltd','2025-10-14 17:30:32'),(3,3,'IBU2024C',200,150,8.00,'2026-01-20','MediSupply Co','2025-10-14 17:30:32'),(4,4,'MET2024D',80,50,12.00,'2025-11-30','HealthCare Suppliers','2025-10-14 17:30:32'),(5,5,'ASP2024E',150,100,3.00,'2025-09-10','Global Pharma','2025-10-14 17:30:32'),(6,6,'OME2024F',90,50,18.00,'2025-10-25','MediSupply Co','2025-10-14 17:30:32'),(7,7,'CIP2024G',25,50,25.00,'2025-07-15','PharmaDist Ltd','2025-10-14 17:30:32'),(8,8,'INS2024H',60,30,850.00,'2025-06-30','Diabetes Care Inc','2025-10-14 17:30:32');
/*!40000 ALTER TABLE `pharmacy_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription_details`
--

DROP TABLE IF EXISTS `prescription_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription_details` (
  `detail_id` int NOT NULL AUTO_INCREMENT,
  `prescription_id` int NOT NULL,
  `medicine_id` int NOT NULL,
  `dosage` varchar(100) DEFAULT NULL,
  `frequency` varchar(100) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `instructions` text,
  PRIMARY KEY (`detail_id`),
  KEY `prescription_id` (`prescription_id`),
  KEY `medicine_id` (`medicine_id`),
  CONSTRAINT `prescription_details_ibfk_1` FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`prescription_id`) ON DELETE CASCADE,
  CONSTRAINT `prescription_details_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicines` (`medicine_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription_details`
--

LOCK TABLES `prescription_details` WRITE;
/*!40000 ALTER TABLE `prescription_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `prescription_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `prescription_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `appointment_id` int DEFAULT NULL,
  `prescription_date` date NOT NULL,
  `diagnosis` text,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prescription_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `appointment_id` (`appointment_id`),
  CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `prescriptions_ibfk_3` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` enum('Nurse','Lab Technician','Pharmacist','Receptionist','Admin','Other') NOT NULL,
  `dept_id` int DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `shift` enum('Morning','Evening','Night') DEFAULT 'Morning',
  `status` enum('Active','On Leave','Resigned') DEFAULT 'Active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`),
  UNIQUE KEY `email` (`email`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vitals_monitoring`
--

DROP TABLE IF EXISTS `vitals_monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vitals_monitoring` (
  `vital_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `recorded_by` int DEFAULT NULL,
  `recorded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `blood_pressure_systolic` int DEFAULT NULL,
  `blood_pressure_diastolic` int DEFAULT NULL,
  `heart_rate` int DEFAULT NULL,
  `temperature` decimal(4,2) DEFAULT NULL,
  `oxygen_saturation` int DEFAULT NULL,
  `respiratory_rate` int DEFAULT NULL,
  `blood_sugar` decimal(5,2) DEFAULT NULL,
  `notes` text,
  `alert_status` enum('Normal','Warning','Critical') DEFAULT 'Normal',
  PRIMARY KEY (`vital_id`),
  KEY `patient_id` (`patient_id`),
  KEY `recorded_by` (`recorded_by`),
  CONSTRAINT `vitals_monitoring_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `vitals_monitoring_ibfk_2` FOREIGN KEY (`recorded_by`) REFERENCES `doctors` (`doctor_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vitals_monitoring`
--

LOCK TABLES `vitals_monitoring` WRITE;
/*!40000 ALTER TABLE `vitals_monitoring` DISABLE KEYS */;
/*!40000 ALTER TABLE `vitals_monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `doctor_performance`
--

/*!50001 DROP VIEW IF EXISTS `doctor_performance`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `doctor_performance` AS select `d`.`doctor_id` AS `doctor_id`,concat(`d`.`first_name`,' ',`d`.`last_name`) AS `doctor_name`,`d`.`specialization` AS `specialization`,`dept`.`dept_name` AS `dept_name`,count(distinct `a`.`appointment_id`) AS `total_appointments`,count(distinct `p`.`prescription_id`) AS `total_prescriptions` from (((`doctors` `d` left join `appointments` `a` on((`d`.`doctor_id` = `a`.`doctor_id`))) left join `prescriptions` `p` on((`d`.`doctor_id` = `p`.`doctor_id`))) left join `departments` `dept` on((`d`.`dept_id` = `dept`.`dept_id`))) group by `d`.`doctor_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `patient_summary`
--

/*!50001 DROP VIEW IF EXISTS `patient_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `patient_summary` AS select `p`.`patient_id` AS `patient_id`,concat(`p`.`first_name`,' ',`p`.`last_name`) AS `patient_name`,`p`.`date_of_birth` AS `date_of_birth`,timestampdiff(YEAR,`p`.`date_of_birth`,curdate()) AS `age`,`p`.`gender` AS `gender`,`p`.`blood_group` AS `blood_group`,`p`.`admission_type` AS `admission_type`,`p`.`status` AS `status`,`ba`.`bed_id` AS `bed_id`,`b`.`bed_number` AS `bed_number` from ((`patients` `p` left join `bed_allocations` `ba` on(((`p`.`patient_id` = `ba`.`patient_id`) and (`ba`.`status` = 'Active')))) left join `beds` `b` on((`ba`.`bed_id` = `b`.`bed_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-02 14:36:13

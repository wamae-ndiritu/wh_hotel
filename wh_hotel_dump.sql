-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: wh_hotel_db
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.20.04.1

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
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `room_id` int NOT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `amount` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,2,1,'2024-07-23','2024-07-31',840),(2,2,8,'2024-05-25','2024-05-27',260);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `constraint`
--

DROP TABLE IF EXISTS `constraint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `constraint` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constraint`
--

LOCK TABLES `constraint` WRITE;
/*!40000 ALTER TABLE `constraint` DISABLE KEYS */;
/*!40000 ALTER TABLE `constraint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `currency` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `code` varchar(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currency`
--

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;
/*!40000 ALTER TABLE `currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_rate`
--

DROP TABLE IF EXISTS `exchange_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_rate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `currency_id` int NOT NULL,
  `date` date NOT NULL,
  `rate` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `currency_id` (`currency_id`),
  CONSTRAINT `exchange_rate_ibfk_1` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_rate`
--

LOCK TABLES `exchange_rate` WRITE;
/*!40000 ALTER TABLE `exchange_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(100) NOT NULL,
  `city_image_url` varchar(255) DEFAULT NULL,
  `capacity` int NOT NULL,
  `peak_season_rate` float NOT NULL,
  `off_peak_rate` float NOT NULL,
  `standard_room_capacity` int DEFAULT NULL,
  `double_room_capacity` int DEFAULT NULL,
  `family_room_capacity` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel`
--

LOCK TABLES `hotel` WRITE;
/*!40000 ALTER TABLE `hotel` DISABLE KEYS */;
INSERT INTO `hotel` VALUES (3,'Birmingham','static/images/Birmingham_.jpeg',110,150,75,NULL,NULL,NULL),(4,'Bristol ','static/images/Bristol_.jpeg',100,140,70,NULL,NULL,NULL),(5,'Cardiff ','static/images/Cardiff_.jpeg',90,130,70,NULL,NULL,NULL),(6,'Edinburgh ','static/images/Edinburgh_.jpeg',120,160,80,NULL,NULL,NULL),(7,'Glasgow ','static/images/Glasgow.jpeg',140,150,75,NULL,NULL,NULL),(8,'London ','static/images/London.jpeg',160,200,100,NULL,NULL,NULL),(9,'Manchester ','static/images/Manchester.jpeg',150,180,90,NULL,NULL,NULL),(10,'New Castle ','static/images/New_Castle.jpeg',90,120,70,NULL,NULL,NULL),(11,'Norwich ','static/images/Norwich.jpeg',90,130,70,NULL,NULL,NULL),(12,'Nottingham ','static/images/Nottingham.jpeg',110,130,70,NULL,NULL,NULL),(13,'Oxford 90','static/images/Oxford.jpeg',90,180,90,NULL,NULL,NULL);
/*!40000 ALTER TABLE `hotel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `price` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `currency_id` int NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `currency_id` (`currency_id`),
  CONSTRAINT `price_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `price_ibfk_2` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price`
--

LOCK TABLES `price` WRITE;
/*!40000 ALTER TABLE `price` DISABLE KEYS */;
/*!40000 ALTER TABLE `price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `hotel_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `room_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,'standard',3),(2,'double',3),(3,'family',3),(4,'standard',4),(5,'double',4),(6,'family',4),(7,'standard',5),(8,'double',5),(9,'family',5),(10,'standard',6),(11,'double',6),(12,'family',6),(13,'standard',6),(14,'standard',7),(15,'double',7),(16,'family',7),(17,'standard',8),(18,'double',8),(19,'family',8),(20,'standard',9),(21,'double',9),(22,'family',9),(23,'standard',10),(24,'family',10),(25,'double',10),(26,'standard',11),(27,'double',11),(28,'family',11),(29,'standard',12),(30,'double',12),(31,'family',12),(32,'standard',13),(33,'double',13),(34,'family',13);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'wamae','wamaejoseph392@gmail.com','12345678'),(2,'ndirituwamae','ndirituwamae@students.uonbi.ac.ke','scrypt:32768:8:1$GeczaJLrCGqSEuy5$0bb055af3bde1e5af8a5b07d03b82f23def7694bd390b94ec27119f32082d9c675b6f9d8b133eac50e779e5eee10e5967f06857a080a17b08f3e782469f1e724');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-01 15:27:09

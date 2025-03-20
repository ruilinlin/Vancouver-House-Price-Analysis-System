-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: vancouver2025
-- ------------------------------------------------------
-- Server version	5.7.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `vancouver2025`
--

/*!40000 DROP DATABASE IF EXISTS `vancouver2025`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `vancouver2025` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `vancouver2025`;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `name` varchar(100) NOT NULL COMMENT 'Config Parameter Name',
  `value` varchar(100) DEFAULT NULL COMMENT 'Config Parameter Value',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Configuration';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
INSERT INTO `config` VALUES (1,'site_logo','upload/logo.png'),(2,'site_name','Vancouver Real Estate 2025'),(3,'site_description','Vancouver Property Market Analysis');
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vancouver_houses`
--

DROP TABLE IF EXISTS `vancouver_houses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vancouver_houses` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `source` varchar(255) DEFAULT NULL COMMENT 'Source URL',
  `title` varchar(255) DEFAULT NULL COMMENT 'Property Title',
  `cover_image` varchar(255) DEFAULT NULL COMMENT 'Main Image URL',
  `living_area` decimal(10,2) DEFAULT NULL COMMENT 'Living Area (sq ft)',
  `price` decimal(12,2) DEFAULT NULL COMMENT 'List Price (CAD)',
  `listed_date` date DEFAULT NULL COMMENT 'Listed Date',
  `property_type` varchar(50) DEFAULT NULL COMMENT 'Property Type',
  `bedrooms` int(11) DEFAULT NULL COMMENT 'Number of Bedrooms',
  `bathrooms` decimal(4,1) DEFAULT NULL COMMENT 'Number of Bathrooms',
  `address` varchar(255) DEFAULT NULL COMMENT 'Property Address',
  `neighborhood` varchar(100) DEFAULT NULL COMMENT 'Neighborhood',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record Creation Time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vancouver_houses`
--

LOCK TABLES `vancouver_houses` WRITE;
/*!40000 ALTER TABLE `vancouver_houses` DISABLE KEYS */;
INSERT INTO `vancouver_houses` VALUES 
(1,'https://www.rew.ca/properties/sample1','Luxury Waterfront Condo','https://images.sample.com/img1.jpg',1250.00,1250000.00,'2025-01-15','Condo',2,2.0,'123 Pacific Street','Coal Harbour','2025-01-15 08:00:00'),
(2,'https://www.rew.ca/properties/sample2','Modern Townhouse','https://images.sample.com/img2.jpg',1800.00,1680000.00,'2025-01-16','Townhouse',3,2.5,'456 Main Street','Mount Pleasant','2025-01-16 09:00:00'),
(3,'https://www.rew.ca/properties/sample3','Detached Family Home','https://images.sample.com/img3.jpg',2500.00,2890000.00,'2025-01-17','House',4,3.0,'789 Oak Street','Kitsilano','2025-01-17 10:00:00'),
(4,'https://www.rew.ca/properties/sample4','Downtown Studio','https://images.sample.com/img4.jpg',500.00,650000.00,'2025-01-18','Condo',0,1.0,'101 Richards Street','Yaletown','2025-01-18 11:00:00'),
(5,'https://www.rew.ca/properties/sample5','Penthouse Suite','https://images.sample.com/img5.jpg',2200.00,3500000.00,'2025-01-19','Condo',3,3.5,'202 Robson Street','Downtown','2025-01-19 12:00:00');
/*!40000 ALTER TABLE `vancouver_houses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `username` varchar(100) NOT NULL COMMENT 'Username',
  `password` varchar(100) NOT NULL COMMENT 'Password',
  `role` varchar(100) DEFAULT 'user' COMMENT 'Role',
  `email` varchar(100) DEFAULT NULL COMMENT 'Email',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation Time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Users';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin123','admin','admin@example.com','2025-01-01 00:00:00');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `market_stats`
--

DROP TABLE IF EXISTS `market_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `market_stats` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `date` date NOT NULL COMMENT 'Statistics Date',
  `neighborhood` varchar(100) NOT NULL COMMENT 'Neighborhood',
  `avg_price` decimal(12,2) DEFAULT NULL COMMENT 'Average Price',
  `median_price` decimal(12,2) DEFAULT NULL COMMENT 'Median Price',
  `total_listings` int(11) DEFAULT NULL COMMENT 'Total Listings',
  `avg_days_on_market` int(11) DEFAULT NULL COMMENT 'Average Days on Market',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record Creation Time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COMMENT='Market Statistics';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_stats`
--

LOCK TABLES `market_stats` WRITE;
/*!40000 ALTER TABLE `market_stats` DISABLE KEYS */;
INSERT INTO `market_stats` VALUES 
(1,'2025-01-01','Downtown',1200000.00,980000.00,156,28,'2025-01-01 00:00:00'),
(2,'2025-01-01','Kitsilano',2100000.00,1850000.00,89,35,'2025-01-01 00:00:00'),
(3,'2025-01-01','Mount Pleasant',1450000.00,1280000.00,112,25,'2025-01-01 00:00:00'),
(4,'2025-01-01','Coal Harbour',2500000.00,2100000.00,67,42,'2025-01-01 00:00:00'),
(5,'2025-01-01','Yaletown',1350000.00,1100000.00,94,31,'2025-01-01 00:00:00');
/*!40000 ALTER TABLE `market_stats` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-01 00:00:00 
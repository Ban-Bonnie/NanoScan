-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2025 at 07:15 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nanoscan`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_accounts`
--

CREATE TABLE `admin_accounts` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_accounts`
--

INSERT INTO `admin_accounts` (`id`, `name`, `username`, `password`) VALUES
(1, 'Bonnie', 'Bonnie132', 'bonnie123'),
(2, 'Ejvind', 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `rfid`
--

CREATE TABLE `rfid` (
  `tag_Id` int(15) NOT NULL,
  `tag_no` varchar(255) NOT NULL,
  `registered` tinyint(1) NOT NULL,
  `admin` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rfid`
--

INSERT INTO `rfid` (`tag_Id`, `tag_no`, `registered`, `admin`) VALUES
(0, '98e0191', 1, 0),
(1, '23646329', 1, 0),
(2, '43907e28', 1, 0),
(3, 'd8ac8790', 1, 1),
(5, '1575f77c', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `section_schedule`
--

CREATE TABLE `section_schedule` (
  `id` int(11) NOT NULL,
  `section` varchar(50) NOT NULL,
  `subject_name` varchar(100) NOT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `subject_teacher` varchar(50) NOT NULL,
  `room` varchar(50) NOT NULL
) ;

--
-- Dumping data for table `section_schedule`
--

INSERT INTO `section_schedule` (`id`, `section`, `subject_name`, `day_of_week`, `start_time`, `end_time`, `subject_teacher`, `room`) VALUES
(1, 'FC1-BSIT2-4', 'People and Earth\'s Ecosystem', 'Friday', '07:30:00', '09:00:00', 'Marjorie Frajilla', 'ML405'),
(2, 'FC1-BSIT2-4', 'Philippine History', 'Friday', '09:00:00', '10:30:00', 'Katrina Bautista', 'ML405'),
(3, 'FC1-BSIT2-4', 'Human Computer Interaction 2', 'Friday', '10:30:00', '12:00:00', 'Krislyn Sinoy', 'ML402'),
(4, 'FC1-BSIT2-4', 'Systems Integration', 'Friday', '06:00:00', '09:00:00', 'Melene Akil', 'CL4'),
(5, 'FC1-BSIT2-4', 'Physical Education ', 'Saturday', '08:00:00', '09:00:00', 'Ria Marquez', 'GYM'),
(6, 'FC1-BSIT2-4', 'Student Success Program', 'Saturday', '09:00:00', '10:00:00', 'Aira Silvestre', 'ML402'),
(7, 'FC1-BSIT2-4', 'App Development', 'Saturday', '11:00:00', '13:30:00', 'Jean Gran', 'CL6'),
(8, 'FC1-BSIT2-4', 'Entrepreneurial Mind', 'Saturday', '15:00:00', '16:30:00', 'Mae Gonzales', 'ML405'),
(9, 'FC1-BSIT2-4', 'Web System and Technologies', 'Saturday', '18:00:00', '21:00:00', 'Marvin Aungon', 'CL1'),
(10, 'CE-101', 'Structural Analysis', 'Monday', '08:00:00', '10:00:00', 'Dr. John Doe', 'A1'),
(11, 'CE-101', 'Fluid Mechanics', 'Tuesday', '10:00:00', '12:00:00', 'Prof. Jane Smith', 'B2'),
(12, 'CE-101', 'Geotechnical Engineering', 'Wednesday', '09:00:00', '11:00:00', 'Dr. Emily Brown', 'C3'),
(13, 'CE-101', 'Transportation Engineering', 'Thursday', '14:00:00', '16:00:00', 'Prof. Mark Wilson', 'D4'),
(14, 'CE-101', 'Concrete Technology', 'Friday', '08:00:00', '10:00:00', 'Dr. Sarah Johnson', 'E5'),
(15, 'CE-101', 'Construction Management', 'Saturday', '13:00:00', '15:00:00', 'Joel Tomado', 'F6');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(15) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `parent_phone` varchar(15) NOT NULL,
  `student_phone` varchar(15) NOT NULL,
  `tag_no` varchar(255) NOT NULL,
  `section` varchar(255) DEFAULT NULL,
  `student_id` varchar(255) NOT NULL,
  `program` varchar(50) NOT NULL,
  `profile` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `first_name`, `last_name`, `parent_phone`, `student_phone`, `tag_no`, `section`, `student_id`, `program`, `profile`) VALUES
(1, 'Bonnie Boy', 'Franco', '09125782910', '09726512344', '23646329', 'CE-101', '04-2324-032584', 'BS Civil Engineering', 'static/img/Bonnie.png'),
(2, 'Ejvind Gem', 'Gimotea', '09125782910', '09726512344', '43907e28', 'FC1-BSIT2-4', '04-2324-033281', 'BS Information Technology', 'static/img/Ejvind.png'),
(5, 'Febbie Jean', 'Pineda', '09125782910', '09726512123', '1575f77c', 'FC1-BSIT2-4', '04-2323-038188', 'BS Information Technology', ''),
(13, 'Reyniel Josh', 'Rojo', '09927162719', '098291728501', '98e0191', 'FC1-BSIT2-4', '04-2324-033877', 'BS Information Technology', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_accounts`
--
ALTER TABLE `admin_accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rfid`
--
ALTER TABLE `rfid`
  ADD PRIMARY KEY (`tag_Id`);

--
-- Indexes for table `section_schedule`
--
ALTER TABLE `section_schedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_tag` (`tag_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_accounts`
--
ALTER TABLE `admin_accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `section_schedule`
--
ALTER TABLE `section_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

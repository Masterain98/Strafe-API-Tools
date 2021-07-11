-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 08, 2021 at 01:15 PM
-- Server version: 10.4.12-MariaDB-log
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `strafe_tools`
--

-- --------------------------------------------------------

--
-- Table structure for table `matches`
--

CREATE TABLE `matches` (
  `matchID` int(11) NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `away_teamID` int(11) NOT NULL,
  `away_team_name` text NOT NULL,
  `home_teamID` int(11) NOT NULL,
  `home_team_name` text NOT NULL,
  `game_type` int(11) NOT NULL,
  `pathID` text NOT NULL,
  `event_name` text NOT NULL,
  `full_path_name` text NOT NULL,
  `match_status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `odds`
--

CREATE TABLE `odds` (
  `matchID` int(11) NOT NULL,
  `record_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `away_odds` double NOT NULL,
  `home_odds` double NOT NULL,
  `tie_odds` double NOT NULL,
  `away_vote_count` int(11) NOT NULL,
  `home_vote_count` int(11) NOT NULL,
  `tie_vote_count` int(11) NOT NULL,
  `stake_result` text NOT NULL,
  `match_result` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

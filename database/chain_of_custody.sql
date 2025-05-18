SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

CREATE TABLE `coc_access` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `eid` int(11) NOT NULL,
  `case_id` varchar(20) NOT NULL,
  `view_st` int(11) NOT NULL,
  `download_st` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_access` (`id`, `uname`, `eid`, `case_id`, `view_st`, `download_st`, `dtime`) VALUES
(1, 'AT1', 1, 'C0220231', 1, 1, '2023-02-17 17:43:11'),
(2, 'AT1', 2, 'C0220231', 1, 2, '2023-02-17 17:51:50'),
(3, 'AT1', 3, 'C0220231', 1, 1, '2023-02-17 17:43:11');

CREATE TABLE `coc_allow` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `case_id` varchar(20) NOT NULL,
  `view_st` int(11) NOT NULL,
  `upload_st` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_allow` (`id`, `uname`, `case_id`, `view_st`, `upload_st`, `dtime`) VALUES
(1, 'AT1', 'C0220231', 1, 1, '2023-02-17 13:12:01'),
(2, 'AT1', 'C0220232', 1, 0, '2023-02-17 13:11:48'),
(3, 'AT2', 'C0220231', 1, 1, '2023-02-17 16:39:19');

CREATE TABLE `coc_attack` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `eid` int(11) NOT NULL,
  `efile` varchar(100) NOT NULL,
  `case_id` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_attack` (`id`, `uname`, `eid`, `efile`, `case_id`, `status`, `dtime`) VALUES
(1, 'AT2', 4, 'E4face16.jpg', 'C0220231', 1, '2023-02-17 17:15:59');

CREATE TABLE `coc_case` (
  `id` int(11) NOT NULL,
  `case_id` varchar(20) NOT NULL,
  `district` varchar(30) NOT NULL,
  `station` varchar(30) NOT NULL,
  `title` varchar(50) NOT NULL,
  `cdate` varchar(20) NOT NULL,
  `details` text NOT NULL,
  `suspect` varchar(200) NOT NULL,
  `name` varchar(100) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `district2` varchar(30) NOT NULL,
  `pincode` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_case` (`id`, `case_id`, `district`, `station`, `title`, `cdate`, `details`, `suspect`, `name`, `fname`, `gender`, `dob`, `address`, `district2`, `pincode`, `mobile`, `email`, `aadhar`, `status`, `dtime`) VALUES
(1, 'C0220231', 'Karur', 'B2', 'Theft', '2023-02-02', 'Jewells Theft', 'customer', 'Prakash', 'Mohan', 'Male', '1986-08-12', 'RR Nagar', 'Karur', '624523', 9632548421, 'praksh@gmail.com', '678967896789', 0, '2023-02-15 21:07:54'),
(2, 'C0220232', 'Thanjavur', 'B5', 'Land Problem', '2023-02-06', '2 group people clash', '-', 'Sivam', 'Ram', 'Male', '1983-02-21', 'DG Nagar', 'Thanjavur', '623497', 8865255441, 'sivam@gmail.com', '554644118833', 0, '2023-02-17 12:35:09');

CREATE TABLE `coc_evidence` (
  `id` int(11) NOT NULL,
  `case_id` varchar(20) NOT NULL,
  `details` varchar(200) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `status` int(11) NOT NULL default 0,
  `upload_by` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_evidence` (`id`, `case_id`, `details`, `filename`, `dtime`, `status`, `upload_by`) VALUES
(1, 'C0220231', 'Bill proof', 'E1coc2.jpg', '2023-02-17 12:22:19', 0, 'admin'),
(2, 'C0220231', 'evidence', 'E2face19.jpg', '2023-02-17 12:21:46', 0, 'admin'),
(3, 'C0220231', 'evidence', 'E3face16.jpg', '2023-02-17 13:18:54', 0, 'AT1'),
(4, 'C0220231', 'my proof', 'E4face16.jpg', '2023-02-17 16:52:40', 0, 'AT2');

CREATE TABLE `coc_login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `block_key` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_login` (`username`, `password`, `block_key`) VALUES
('admin', 'admin', 'bcoc2131');

CREATE TABLE `coc_register` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `designation` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `location` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_register` (`id`, `name`, `designation`, `mobile`, `email`, `aadhar`, `location`, `city`, `uname`, `pass`, `status`, `dtime`) VALUES
(1, 'Ramkumar', 'Junior Advocate', 8896377412, 'ramkumar@gmail.com', '432156784321', 'FF Nagar', 'Salem', 'AT1', '123456', 1, '2023-02-15 21:00:40'),
(2, 'Dharun', 'Police', 8875644231, 'dharun@gmail.com', '256344848454', 'DG Road', 'Karur', 'AT2', '123456', 1, '2023-02-15 21:02:59');

CREATE TABLE `coc_request` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `message` varchar(200) NOT NULL,
  `reply` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `cname` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `coc_request` (`id`, `uname`, `message`, `reply`, `status`, `dtime`, `cname`) VALUES
(1, 'AT1', 'Evidence ID:2, Case ID:C0220231, File: E2face19.jpg, Download Request by AT1', 'ok', 1, '2023-02-17 15:42:43', ''),
(2, 'admin', 'proof required', '', 1, '2023-02-17 16:15:05', 'AT1'),
(3, 'AT1', 'Evidence ID:3, Case ID:C0220231, File: E3face16.jpg, Download Request by AT1', '', 1, '2023-02-17 17:40:48', '');

ALTER TABLE `coc_access` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_allow` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_attack` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_case` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_evidence` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_login` ADD PRIMARY KEY (`username`);
ALTER TABLE `coc_register` ADD PRIMARY KEY (`id`);
ALTER TABLE `coc_request` ADD PRIMARY KEY (`id`);

ALTER TABLE `coc_access` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `coc_allow` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `coc_attack` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
ALTER TABLE `coc_case` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
ALTER TABLE `coc_evidence` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
ALTER TABLE `coc_register` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
ALTER TABLE `coc_request` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

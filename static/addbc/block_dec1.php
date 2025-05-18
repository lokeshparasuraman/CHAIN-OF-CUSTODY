<?php
session_start();
include("dbconnect.php");
extract($_REQUEST);

$fp=fopen("key.txt","r");
$key=fread($fp,filesize("key.txt"));
fclose($fp);

?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Health Chain</title>
<style type="text/css">
.bor
{
border-bottom:dotted #999999 1px;
}
</style>
</head>

<body>
<p>&nbsp;</p>
<h3 align="center">Block Information</h3>

<p>&nbsp;</p>

	<form name="form1" method="post">
	<p align="center"><input type="text" name="case" placeholder="Case ID" value="<?php echo $case; ?>" />
<input type="submit" name="btn2" value="Search" /></p>
	</form>
	<?php

	$q="";
		if($case!="")
		{
		$q=" where vdata like '%$case%'";
		}
$q1=mysqli_query($connect,"select * from coc_chain_hash $q");
while($r1=mysqli_fetch_array($q1))
{

$i++;

$ss=explode(",",$r1['vdata']);
$tt=explode(":",$ss[1]);
$uu=$tt[1];

			$x1=explode(",",$r1['vdata']);
			$x2=explode(":",$x1[2]);
			$dd=$x2[1];
			
			if($dd=="Attack Found")
			{
			$color="#003366";
			}
			else
			{
			$color="#FF33CC";
			}
												
														
	?>
	<table width="100%" cellpadding="5" cellspacing="5">
	<tr>
	<td width="18%" align="left" style="color:#0066FF">Block ID</td>
	<td width="82%" align="left" style="color:#FF33CC">: <?php echo $i; ?></td>
	</tr>
	<tr>
	<td align="left" style="color:#0066FF">Data</td>
	<td align="left" style="color:<?php echo $color; ?>">: <?php echo $r1['vdata']; ?></td>
	</tr>
	
	
</table>
	<?php
	
}


?>
</body>
</html>

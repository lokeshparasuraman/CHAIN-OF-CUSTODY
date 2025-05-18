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

<p align="center">
<input type="password" name="kk" value="<?php echo $kk; ?>" />
<input type="submit" name="btn" value="Decrypt" />
</p>
</form>
<?php
if(isset($btn))
{
	if($kk==$key)
	{
	?>
	<script language="javascript">
	window.location.href="block_dec1.php";
	</script>
	<?php
	}
	else
	{
	?><p align="center" style="color:#FF0000">Wrong Key!</p><?php
	}
}
?>
</body>
</html>

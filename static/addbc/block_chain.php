<?php
 
$key="xyz123";
	function addBlock($bc,$bid,$pre,$data,$dtime)
	{
	$fn=$bc."_data.json";
	$hash=md5($data);
	 
		if($bid=="1")
		{
		$response = array("block_id"=>$bid,"pre_hash"=>$pre,"hash"=>$hash,"date"=>$dtime);
		$res[]=$response;
		$fp = fopen("data/".$fn, 'w');
		fwrite($fp, json_encode($res));
		fclose($fp);
		
		include("dbconnect.php");
		$mq=mysqli_query($connect,"select max(id) from coc_chain_hash");
		$mr=mysqli_fetch_array($mq);
		$id=$mr['max(id)']+1;
		
		mysqli_query($connect,"insert into coc_chain_hash(id,bcode,hdata,vdata) values($id,'$bc','$hash','$data')");
		
		
		}
		else
		{
		$response = array("block_id"=>$bid,"pre_hash"=>$pre,"hash"=>$hash,"date"=>$dtime);
		$inp = file_get_contents("data/".$fn);
		$tempArray = json_decode($inp);
		array_push($tempArray, $response);
		$jsonData = json_encode($tempArray);
		
		file_put_contents("data/".$fn, $jsonData);
		
		include("dbconnect.php");
		$mq=mysqli_query($connect,"select max(id) from coc_chain_hash");
		$mr=mysqli_fetch_array($mq);
		$id=$mr['max(id)']+1;
		
		mysqli_query($connect,"insert into coc_chain_hash(id,bcode,hdata,vdata) values($id,'$bc','$hash','$data')");
	 
		}
	
	}
	
?>
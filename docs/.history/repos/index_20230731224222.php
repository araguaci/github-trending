<?php
if (session_id() == "")
    session_start();
ob_start();
?>
<?php
    // NOTICE THAT THERE IS NO WHITE-SPACE OR OUTPUT BEFORE <?php
    // AND ALSO; NO "echo" STATEMENT AT ALL BEFORE THE if(isset()){} BLOCK.

    if(isset($_GET['file'])){
        $file = htmlspecialchars(trim($_GET['file']));
        //echo $file;
        //die();
        processDownload($file);
    }

    function processDownload($fileName) {
        if($fileName){
            $dldFile    = $fileName;
            if(file_exists($fileName)){
                $size       = @filesize($fileName);
                header('Content-Description: File Transfer');
                header('Content-Type: application/octet-stream');
                header('Content-Disposition: attachment; filename=' . $fileName);
                header('Content-Transfer-Encoding: binary');
                header('Connection: Keep-Alive');
                header('Expires: 0');
                header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
                header('Pragma: public');
                header('Content-Length: ' . $size);
                return TRUE;
            }
        }
        return FALSE;
    }

?>
<?php
// Page créé par Shepard [Fabian Pijcke] <Shepard8@laposte.net>
// et Romain Bourdon <romain@anaska.com>
// pour WAMP5
//afficher phpinfo
if (isset($_GET['phpinfo'])) {
    phpinfo();
    exit();
}
?>
<?php
    echo "<pre>";
	$handle = opendir(".");
	$cnt = 0;
	while ($file = readdir($handle)) {
        $file = strtolower($file);
		    if (substr($file, -2)=="md") {
          echo '
    - [' . str_replace('.md', '', $file) . '](/repos/' . $file . ')';
        }
	}
	closedir($handle);
	/*
	echo "<pre>";
	print_r($alias);
	echo "</pre>";
	die();
	*/
    echo "</pre>";


//Verifica o Proxy e retorna o ip real
function getRealIPAddress() {

    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        //check ip from share internet
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } else if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        //to check ip is pass from proxy
        $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}

//retorna nome da máquina remota pelo IP
function NomeMaquinaRem() {

    $Nome = gethostbyaddr(getRealIPAddress());
    return $Nome;
}

//Mac da Máquina remota conectada
function MacAdressByWindows() {

    $ipAddress = getRealIPAddress();

    #run the external command, break output into lines
    exec("arp -a $ipAddress", $output);
    $IpMac = explode(" ", trim($output[3]));
    return $IpMac[11];
}

function getMacAddress() {
    ob_start();
    system('getmac /NH');
    $mycom = ob_get_contents();
    $mycom = str_replace("N/A", "", $mycom);
    $mycom = str_replace("Hardware ausente", "", $mycom);
    $mycom = cleanString($mycom);
    ob_clean();
    $pmac = strpos($mycom, "\Device");
    $mac = substr($mycom, $pmac - 20, 20);
    $mac = trim(ew_RemoveCrLf($mac));
    return trim(ew_RemoveCrLf($mac));
}

function getCPUInfo() {
    ob_start(); // Turn on output buffering
    system('VOL'); //Execute external program to display output
    $mycom = ob_get_contents(); // Capture the output into a variable
    ob_clean(); // Clean (erase) the output buffer
    $findme = "-";
    $pmac = strpos($mycom, $findme); // Find the position of Physical text
    $mac = trim(substr($mycom, -12, $pmac)); // Get Physical Address
    return str_replace("-", "", $mac);
}

// encrypt
function TEAencrypt($str, $key = '6oL5scK4Muiy9h64') {
    if ($str == "") {
        return "";
    }
    $v = str2long($str, true);
    $k = str2long($key, false);
    $cntk = count($k);
    if ($cntk < 4) {
        for ($i = $cntk; $i < 4; $i++) {
            $k[$i] = 0;
        }
    }
    $n = count($v) - 1;
    $z = $v[$n];
    $y = $v[0];
    $delta = 0x9E3779B9;
    $q = floor(6 + 52 / ($n + 1));
    $sum = 0;
    while (0 < $q--) {
        $sum = int32($sum + $delta);
        $e = $sum >> 2 & 3;
        for ($p = 0; $p < $n; $p++) {
            $y = $v[$p + 1];
            $mx = int32((($z >> 5 & 0x07ffffff) ^ $y << 2) + (($y >> 3 & 0x1fffffff) ^ $z << 4)) ^ int32(($sum ^ $y) + ($k[$p & 3 ^ $e] ^ $z));
            $z = $v[$p] = int32($v[$p] + $mx);
        }
        $y = $v[0];
        $mx = int32((($z >> 5 & 0x07ffffff) ^ $y << 2) + (($y >> 3 & 0x1fffffff) ^ $z << 4)) ^ int32(($sum ^ $y) + ($k[$p & 3 ^ $e] ^ $z));
        $z = $v[$n] = int32($v[$n] + $mx);
    }
    return ew_UrlEncode(long2str($v, false));
}

// decrypt
function TEAdecrypt($str, $key = '6oL5scK4Muiy9h64') {
    $str = ew_UrlDecode($str);
    if ($str == "") {
        return "";
    }
    $v = str2long($str, false);
    $k = str2long($key, false);
    $cntk = count($k);
    if ($cntk < 4) {
        for ($i = $cntk; $i < 4; $i++) {
            $k[$i] = 0;
        }
    }
    $n = count($v) - 1;
    $z = $v[$n];
    $y = $v[0];
    $delta = 0x9E3779B9;
    $q = floor(6 + 52 / ($n + 1));
    $sum = int32($q * $delta);
    while ($sum != 0) {
        $e = $sum >> 2 & 3;
        for ($p = $n; $p > 0; $p--) {
            $z = $v[$p - 1];
            $mx = int32((($z >> 5 & 0x07ffffff) ^ $y << 2) + (($y >> 3 & 0x1fffffff) ^ $z << 4)) ^ int32(($sum ^ $y) + ($k[$p & 3 ^ $e] ^ $z));
            $y = $v[$p] = int32($v[$p] - $mx);
        }
        $z = $v[$n];
        $mx = int32((($z >> 5 & 0x07ffffff) ^ $y << 2) + (($y >> 3 & 0x1fffffff) ^ $z << 4)) ^ int32(($sum ^ $y) + ($k[$p & 3 ^ $e] ^ $z));
        $y = $v[0] = int32($v[0] - $mx);
        $sum = int32($sum - $delta);
    }
    return long2str($v, true);
}

function ew_UrlEncode($string) {
    $data = base64_encode($string);
    return str_replace(array('+', '/', '='), array('-', '_', '.'), $data);
}

function str2long($s, $w) {
    $v = unpack("V*", $s . str_repeat("\0", (4 - strlen($s) % 4) & 3));
    $v = array_values($v);
    if ($w) {
        $v[count($v)] = strlen($s);
    }
    return $v;
}

function int32($n) {
    while ($n >= 2147483648)
        $n -= 4294967296;
    while ($n <= -2147483649)
        $n += 4294967296;
    return (int) $n;
}

function long2str($v, $w) {
    $len = count($v);
    $s = array();
    for ($i = 0; $i < $len; $i++) {
        $s[$i] = pack("V", $v[$i]);
    }
    if ($w) {
        return substr(join('', $s), 0, $v[$len - 1]);
    } else {
        return join('', $s);
    }
}

function ew_UrlDecode($string) {
    $data = str_replace(array('-', '_', '.'), array('+', '/', '='), $string);
    return base64_decode($data);
}

/*
 * clearstring
 */
function cleanString($str, $charlist = '') {
    $result = '';
    /* list of forbidden chars to be trimmed */
    $forbidden_list = array("\t", "\r", "\n", "\0", "\x0B");

    if (empty($charlist)) {
        for ($i = 0; $i < strlen($str); $i++) {
            if (($str[$i] != $forbidden_list[0]) &&
                    ($str[$i] != $forbidden_list[1]) &&
                    ($str[$i] != $forbidden_list[2]) &&
                    ($str[$i] != $forbidden_list[3]) &&
                    ($str[$i] != $forbidden_list[4]) &&
                    ($str[$i] != $forbidden_list[5])) {
                $result .= $str[$i];
            }
        }
    } else if (!empty($charlist)) {
        $is_not_same = true;

        for ($i = 0; $i < strlen($str); $i++) {
            for ($j = 0; $j < strlen($charlist); $j++) {
                if ($str[$i] != $charlist[$j]) {
                    $is_not_same = true;
                } else if ($str[$i] == $charlist[$j]) {
                    $is_not_same = false;
                    break;
                }
            }

            if ($is_not_same == true) {
                $result .= $str[$i];
            }
        }
    }

    return ($result);
}

function ew_RemoveCrLf($s) {
    if (strlen($s) > 0) {
        $s = str_replace("\n", " ", $s);
        $s = str_replace("\r", " ", $s);
        $s = str_replace("\l", " ", $s);
        $s = str_replace("  ", " ", $s);
    }
    return $s;
}

function createPath($title) {
    if ($title=='') {
        $title = "TOP";
    }
    $path = $_SERVER['SCRIPT_FILENAME'];
    $path = str_replace('/', '\\', $path);
    $path = str_replace('\\_', '\\', $path);
    $path = str_replace('index.php', '', strtolower($path));
	$path = str_replace('_index.php', '', strtolower($path));
    return '&nbsp;' . strtolower($path) . '&nbsp;&nbsp;<a href="#' . $title . '" title="' . $title . '"><img src="http://localhost/apps/images/network.png" align="absmiddle"/></a>';
}

?>
<?php
//echo "<pre><code>";
//print_r ($_SERVER);
//echo "</code></pre>";
?>

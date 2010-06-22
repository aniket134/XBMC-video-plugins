<?
include("english_text.php");



function translate2($text) {
    $lp = "en|hi";
    $in = file_get_contents("http://google.com/translate_t?langpair=".urlencode($lp)."&text=".urlencode($text)) or die("false");
    return $in;
}



function extract_result($raw) {
    #
    # look for this: 
    # <input type=hidden id=nc_text value="hello">
    # 
    # and for this:
    # <input type=hidden name=gtrans value="hallo">
    #
    #$quesRegEx = '/<input type=hidden id=nc_text value="([^<>]*)">/';
#    if (preg_match($quesRegEx, $raw, $matchQues)) {
#	echo $matchQues[1];
#    } else {
#	echo "failed to find question.\n";
#    }

    $ansRegEx = '/<input type=hidden name=gtrans value="([^<>]*)">/';

    if (preg_match($ansRegEx, $raw, $matchAns)) {
	return $matchAns[1];
    }
    echo "failed to find match.\n";
    return '';
}



function main() {
    global $trans_source;

    $outf = fopen("google_english2hindi.py", "w");
    fwrite($outf, "# -*- coding: latin-1 -*-\n");
    fwrite($outf, "GOOGLE_AUTO_DICT = {\n");
    $num = 0;

    foreach ($trans_source as $chksum => $english) {
	echo "    [English is:] " . $english . "\n";
	echo "    [" . $num . ". querying Google...]\n";
	$raw = translate2($english);
	$ans = extract_result($raw);
	$output = '"' . $chksum . '"' . ' : ' . '"' . $ans . '",' . "\n";
	fwrite($outf, $output);
	echo $output;
	$rDelay = rand(0, 40);
	$rDelay += 15;
	echo "------------------------------------------------------------\n";
	echo "\n";
	echo "    [sleeping " . $rDelay . " s...]\n";
	sleep($rDelay);
	$num++;
    }

    fwrite($outf, "}\n");
    fclose($outf);
    exit(0);


}



main();
?>

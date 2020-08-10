$ffmpeg = "C:/path/to/ffmpeg.exe"
$eventname = "2020Llandow"
$videosuffix = "MP4"

If (Test-Path "ffmpeg.bat") {Remove-Item "ffmpeg.bat" -Force}
ForEach ($folder in (Get-ChildItem -Path . -Directory)) {
    If (Test-Path "$($folder.FullName)\files.txt") {Remove-Item "$($folder.FullName)\files.txt" -Force}
    ForEach ($MP4 in (Get-ChildItem -Path $folder.FullName -Filter *.$videosuffix)) {
        "file $($folder.Name)/$($MP4.Name)" | Out-File "$($folder.FullName)\files.txt" -Append -Encoding ascii
    }
    "$ffmpeg -f concat -i $($folder.FullName)\files.txt -c copy $eventname-$($folder.Name).$videosuffix" | Out-File -FilePath ffmpeg.bat -Append -Encoding ascii
    #-filter:v "setpts=0.95*PTS"
}
& ffmpeg.bat
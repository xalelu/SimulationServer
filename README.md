# SimulationServer
模擬sensor回傳modbus/http response
用於模擬設備端/伺服端回應歷史資料數值, 以測試自動下載CSV檔專案功能
- 步驟1: 
  <p>在cmd下, 進入到virtualDevice.py所在位置, 輸入python virtualDevice.py(可能僅支援python3), 即可啟動偵聽504port的伺服器</p>
  
- 步驟2:
  <p>開啟postman之類軟體, 鍵入http://主機ip:504/data.csv?&start=2021-10-10-10-10&end=2021-10-11-10-10&interval=80, method選定Get, HTTP HEADER加入Content-Type: Text/csv 
  url參數說明:start/end:指定要抓取start(開始時間)到end(結束時間)的資料, interval為紀錄間隔, 上述參數即要抓取2021年10月10日 10點10分 到 2021年10月11日 10點10分之間的資料
  每筆資料間隔80秒</p>
  
- 注意: 該伺服器取得的數值資料, 皆是亂數產生, 僅用於測試用

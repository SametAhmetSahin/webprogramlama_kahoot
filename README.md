# Kahoot Klonu

Kocaeli Üniversitesi Web Programlama dersinin vize ödevi olarak aşağıdaki öğrenciler tarafından yapılan  
```
210201041 - Samet Ahmet Şahin  
210201077 - Taha Furkan Genç  
210201033 - Mehmet Ali Kır  
210201096 - Alperen Karacan  
```
bu projede öğretmenlerin sınıflarını test edebileceği online bir quiz platformu geliştirilmiştir.
Backendde API-first ve RESTful API yaklaşımı izlenmekte, bir kullanıcının login olmasıyla beraber verilen tokenle istekler gerçekleştirilmekte, tokenin doğrulaması yapılmaktadır. Tarayıcı üzerinden yapılan girişlerde token cookielerde tutulmakta, logoutta sıfırlanmaktadır.
## Register ve Login
Web sitesine girişte token sorgulanmakta, eğer yoksa veya expire olmuşsa kullanıcı login sayfasına yönlendirilmektedir. Login sayfasından register sayfasına geçilebilir.
## Ana Sayfa
Kayıt olma ve giriş yapma işlemlerinin gerçekleştirilmesinden sonra kullanıcıyı quizleri görebileceği, kullanıcıları görebileceği ve logout olabileceği bir ana sayfa karşılamaktadır. 
## Kullanıcıları Görüntüle
Kullanıcıları görüntüleme yetkisi sadece Admin kullanıcısı için bulunmaktadır.
## Quizler Sayfası
Quizler sayfasına geçildiğinde veritabanında bulunan tüm quizler sahipleri, soru adedi ve görüntüle ile quizi başlat seçenekleriyle listelenir. Ayrıca Quiz oluştur butonu bulunmaktadır. 
## Quizi Görüntüle
Quizi görüntüle seçeneğine tıklanıldığında quizdeki sorular, bu soruların doğru cevapları ve quizdeki doğru/yanlış cevap oranlarının soru bazında grafiğe dökülmüş hali görülebilir. Bu sayfadan quiz sayfasına geri dönülebilir.
## Quiz Oluşturma
Quizin adı, ilk soru, sorunun yazısı, AI ile oluşturma seçeneği ve AI'dan istenen soru türünün yazılacağı ayrıca cevapların yazılacağı ve hangi cevabın doğru olduğunu belirten checkboxlar bulunmaktadır. Birden fazla doğru cevap olabilir.
## Quiz Başlatma
Quiz başlatılınca 6 haneli bir sayı verilir, quiz oynama kısmında hesap açmayan öğrenciler tarafından bu sayı girilerek quiz soruları cevaplanabilir.
## Quiz Oynama
Öğretmen tarafından verilen 6 haneli sayı girilip quiz başlata tıklanınca sorular sırayla öğrencinin karşısına gelir. Son sorunun cevaplanmasıyla beraber istatistikler servera gönderilir.
## Notlar
AI ile soru oluşturmanın çalışması için projenin root klasöründe `gemini_key.txt` adında içinde Gemini API keyi olan bir dosya konulması gerekmektedir.  
Web arayüzü 8004 portunda çalışmaktadır.
Quiz oynama urlsi: `http://host:8004/playquiz`
Quiz oynama için giriş gerekmemesi özellikle yapılmıştır.
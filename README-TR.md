#### Other Languages: [English](https://github.com/MERT-CKR/Sky-Instrument-Player/blob/main/README.md)

---
## Bu uygulama, Steam platformundaki "Sky: Children of the Light" isimli oyundaki enstrümanları otomatik olarak çalmak için tasarlandı. 

## YouTube'da izleyin👁️↓
[![watch on YT](https://i3.ytimg.com/vi/ZUfYclM6AHA/maxresdefault.jpg)](https://www.youtube.com/watch?v=ZUfYclM6AHA)




#### Programın çalışabilmesi için:
* [Python](https://www.python.org)'un bilgisayarınızda yüklü olduğundan emin olun.
### Aşağıdaki kütüphaneleri yüklemeniz gerekmektedir:
* pandas 
* keyboard


Bu kütüphaneleri komut satırı arayüzünde(CMD) aşağıdaki komutları kullanarak yükleyin:

```cmd
pip install pandas
```

```cmd
pip install keyboard
```

## Kullanım:

Program ilk açıldığında sizden dil seçmenizi isteyecektir.

Sadece Türkçe ve ingilizce dil destekleri mevcut


### Programı hangi ortamda kullanacağınıza bağlı olarak tuş kombinasyonunu seçmeniz gerekmektedir:

#### 1. Eğer `Sky Music Nightly` sitesindeki enstrümanları kullanıyorsanız, şu tuş kombinasyonunu kullanabilirsiniz:

`
q w e r t a s d f g z x c v b
`

#### 2. Eğer oyundaki enstrümanı kullanıyorsanız:
* Oyundaki enstrümanı kuşandığınızda butonların üzerinde yazan harfleri, aralarında boşluk olacak şekilde girin. 

* Bu tuşlar Arasında nokta veya virgül karakterleri varsa bunları Ayarlar > Kontroller kısmından başka bir tuşla değiştirin. (öneri: b)


### Eğer uygulamayı indirdiyseniz, oyun olmadan [Sky Music Nightly](https://specy.github.io/skyMusic/) sitesinde test edebilirsiniz.

---

## Önemli not!

* Listeden müziğinizi seçip enstrüman çalacağınız pencereye odak verin. Bu kısımda biraz dikkatli olmalısınız; eğer odağı başka bir pencereye verirseniz rastgele tuşlara basılacaktır, bu da istenmeyen durumları tetikleyebilir. 

* Örneğin, eğer odağı bir metin belgesine verirseniz, oraya yazı yazacaktır. Bu yüzden müzik çalma sürecinde odağı hedef pencerede tuttuğunuzdan emin olun. Müzik çalma sürecini iptal etmek için ise `"` tuşuna müzik durana kadar basılı tutun

---
### Dil seçimini veya tuş atamalarını değiştirmek için:
* `reset key settings.py` dosyasını çalıştırın.



## Başka müzikler listeye nasıl eklenir?

* ### Eğer zaten notalarınız varsa
    * Notalarınızı `New Sheets`klasörüne kopyalayın 
    * Nota dosyanızda sadece 1 katman olduğundan emin olun

* ### Eğer notalarınız yoksa
    * `Sky-Auto Instrument Player.py` ile aynı dizinde bulunan `SongDatabase` klasöründen istediğiniz müzik notalarını kopyalayıp `New Sheets` klasörüne yapıştırın. Sonrasında Programı açın veya yeniden başlatın.

* ### Desteklenen nota formatları
    * `.txt`
    * `.json`
    * `.skysheet`

* Eğer notalarınızı `New Sheets` klasörüne kopyaladıysanız ve orijinal dosyaları bulamıyorsanız `Raw Sheets` klasörüne bakın.

* Eğer `New Sheets` veya `Raw Sheets` klasörünü bulamıyorsanız programı bir kez çalıştırın Otomatik olarak oluşturulacaktır.



* Tek seferde çok fazla dosyayı aynı anda eklemeniz önerilmiyor. Ayrıca, `New Sheets` klasörüne attığınız dosyaların içinde Japonca veya başka dilde karakterler varsa hata verebilir. Bu karakterleri silip tekrar denerseniz düzelecektir.


* `Sheets` klasöründe, listedeki müzikler bulunmaktadır. Eğer isterseniz, onları yeniden adlandırabilirsiniz veya kaldırabilirsiniz.


---

### Aradığınız şeyi bulamadınız mı?
* `Auto-Insturment Player` için Wiki üzerinde çalışıyorum 
* Discorddan bana ulaşın: luvica0


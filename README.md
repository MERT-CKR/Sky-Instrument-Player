## Bu uygulama Steam platformundaki `Sky: Children of the Light` isimli oyundaki enstrümanları otomatik çalmak için tasarlandı 

### [Eğer uygulamayı indirdiyseniz oyun olmadan bu sitede de test edebilirsiniz](https://specy.github.io/skyMusic/)





#### Programın çalışabilmesi için:
### Python'un bilgisayarınızda yüklü oduğundan emin olun
Aşağıdaki kütüphaneleri yüklemeniz gerekmektedir:
* pandas 
* keyboard


Bu kütüphaneleri komut satırı arayüzünüzde aşağıdaki komutları kullanarak yükleyin:

```cmd
pip install pandas
```

```cmd
pip install keyboard
```

### kullanım:

progarm ilk açıldığında sizden dil seçmenizi isteyecektir.


## programı hangi ortamda kullanacağınıza bağlı olarak tuş kombinasyonunu seçmeniz gerekmektedir

### 1. Eğer internet sitesindeki enstrümanları kullanıyorsanız bu tuş kombinasyonunu kullanabilirsiniz

`
q w e r t a s d f g z x c v b
`

### 2. eğer oyundaki enstrümanı kullanıyorsanız
Oyundaki enstrümanı kuşandığında butonların üzerinde yazan harfleri sırasıyla aralarında boşluk olacak şekilde girin.

Aralarında nokta veya virgül karakterleri varsa onu Ayarlar>kontroller kısmından başka bir tuşla değitirin.

---

### Önemli not
Listeden müziğinizi seçip odağı enstürman çalacağınız pencereye verin.

Bu kısımda biraz dikkatli olmalısınız eğer odağı başka bir yere verirseniz rastgele tuşlara basılacaktır bu da istenmeyen durumları tetikleyebilir.

Mesela, eğer odağı bir metin belgesine verirseniz oraya yazı yazacaktır. bu yüzden müzik çalma sürecinde odağı hedef pencerede tuttuğunuzdan emin olun.

Müzik çalma sürecini iptal etmek için ise `"` tuşuna ard arda birkaç kez basın.

---
### Başka müzikleri listeye ekleme 

`Sky-Auto Instrument Player.py` ile aynı dizinde SongDatabase isimli içerisinde müziklerin bulunduğu bir klasör var istediklerinizi kopyalayıp 
`New Sheets` isimli klasöre yapıştırın. programı yeniden başlatın veya açın.

Eğer `New Sheets` isimli bir klasör yoksa uygulamayı çalıştırdığınızda otomatik olarak gelecektir.

Tek seferde çok fazla dosyayı aynı anda eklemeniz önerilmiyor. Ayrıca `New Sheets` klasörüne attığınız dosyaların içinde japonca veya bunun gibi başka dilde karakterler varsa hata verebilir. O karakterleri silip tekrar denerseniz düzelecektir.

Dil seçimini veya tuş seçimini değiştirmek için: `reset key settings.py` dosyasını çalıştırın.


`Sheets` klasöründe listedeki müzikler bulunuyor eğer isterseniz onları yeniden adlandırabilirsiniz.

---

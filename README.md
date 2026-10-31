# Harita

**Türkçe** | [English](README.en.md)

> Yapay zekâya rapor yazdırma, harita çizdir.

Yapay zekâ cevabını düz yazı olarak verir, senin beynin ise dallanarak düşünür. **Harita**, herhangi bir içeriği tıklanabilir bir zihin haritasına çeviren bir yapay zekâ becerisidir (skill). Bütünü bir bakışta görürsün, ayrıntıya yalnızca istediğinde inersin.

"Bunu haritala", "zihin haritası çiz" ya da "geçen hafta konuştuklarımızı haritala" demen yeterli.

- Tek dosyalık HTML sayfası üretir; internet bağlantısı ya da kurulum gerekmez.
- Altı düzen: zihin haritası, mantık şeması, ağaç, zaman çizelgesi, balık kılçığı, matris.
- Dalları katlama, tek dala odaklanma, dal dal sunum, telefonda liste görünümü.
- Claude uygulamasında, Codex'te ve Claude Code'da çalışır.

## Kurulum

### Claude uygulaması (claude.ai, masaüstü)

Uygulama GitHub'dan kurmuyor, beceri zip olarak yükleniyor.

1. [`dist/zihin-haritasi.zip`](dist/zihin-haritasi.zip) dosyasını indir (açma, zip olarak kalsın).
2. Ayarlar → Yetenekler bölümünde **Kod çalıştırma ve dosya oluşturma** açık olsun.
3. Özelleştir → Beceriler → **+** → **Beceri yükle** → zip'i seç.
4. Yeni bir sohbette: "Bunu zihin haritası olarak çiz."

Menü adları uygulama sürümüne göre biraz değişebilir.

### Claude Code

Claude Code içinde:

```
/plugin marketplace add leodavincs/harita
/plugin install harita@harita
```

### Codex (uygulama, CLI, IDE)

Codex'e yaz:

```
$skill-installer https://github.com/leodavincs/harita/tree/main/skills/zihin-haritasi
```

Elle kurmak istersen: `skills/zihin-haritasi` klasörünü `~/.agents/skills/` içine kopyala.

## Nasıl çalışır

```
sen: "bunu haritala"
  → yapay zekâ içeriği bir ağaç olarak yazar (JSON)
  → scripts/kur.py veriyi denetler ve tek dosyalık HTML üretir
  → haritayı açarsın; değişiklik istersen aynı dosya yeniden kurulur
```

Veri biçimi: [`skills/zihin-haritasi/references/bicim.md`](skills/zihin-haritasi/references/bicim.md). Bütün özellikleri gösteren örnek: [`examples/ornek.json`](examples/ornek.json).

Elle denemek için:

```sh
python3 skills/zihin-haritasi/scripts/kur.py examples/ornek.json --ac
```

## Lisans

MIT. Dilediğin gibi kullan, değiştir, paylaş.

var tanggalElement = document.getElementById("tanggal");
var waktuElement = document.getElementById("waktu");

// Membuat objek tanggal dan waktu
var sekarang = new Date();

// Mendapatkan tanggal, bulan, tahun, jam, menit, dan detik
var tanggal = sekarang.getDate();
var bulan = sekarang.getMonth() + 1; // Penambahan 1 karena bulan dimulai dari 0 (0 = Januari, 1 = Februari, dst.)
var tahun = sekarang.getFullYear();
var jam = sekarang.getHours();
var menit = sekarang.getMinutes();
var detik = sekarang.getSeconds();

// Format tanggal dan waktu dengan "DD/MM/YYYY" dan "HH:MM:SS"
var tanggalFormat = tanggal + "/" + bulan + "/" + tahun;
var waktuFormat = jam + ":" + menit + ":" + detik;

// Mengatur teks dalam elemen <p> dengan tanggal dan waktu
tanggalElement.textContent = "Tanggal: " + tanggalFormat;
waktuElement.textContent = "Waktu: " + waktuFormat;
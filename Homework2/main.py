import JpegCompress
import JpegDecompress

# 计算压缩率
def computeCompressionRatio():
    pass

# 计算失真度
def computeDistortionRatio():
    
    pass

if __name__ == "__main__":
    # Compress
    compress1 = JpegCompress.Compress('./src/cartoon.jpg')
    compress2 = JpegCompress.Compress('./src/animal.jpg')
    compressedData1 = compress1.getCompressedData()
    compressedData2 = compress2.getCompressedData()
    # Decompress
    decompress1 = JpegDecompress.Decompress(compressedData1, './res/cartoon.jpg')
    decompress2 = JpegDecompress.Decompress(compressedData2, './res/animal.jpg')
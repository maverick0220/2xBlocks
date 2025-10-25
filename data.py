import chessboard
class Data:
    def __init__(self, value, rank):
        self.value = value
        self.rank = rank

        self.color = "#B5B5B5"  # default grey
        self.color = self.getColor()

    def upgradeRank(self):
        ranks = list("abcdfeghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.rank = ranks[ranks.index(self.rank)+1]

    def getColor(self):
        def num_hash(s: float) -> int:
            base = 10  # 数字字符串基于10进制
            mod = 2003  # 大于200的质数，确保连续数字哈希差为1（模2003）
            hash_val = 0
            for c in str(s):
                hash_val = (hash_val * base + int(c)) % mod  # 滚动哈希
            return hash_val

        # 2. 字母字符串哈希（区分不同字母组合）
        def rank_hash(s: str) -> int:
            base = 26  # 小写字母共26个
            mod = 199  # 质数，与200互质增强分布均匀性
            hash_val = 0
            for c in s:
                # 字母a→1, b→2...避免空字符串干扰
                hash_val = (hash_val * base + (ord(c) - ord('a') + 1)) % mod
            return hash_val

        if self.value == -1:
            return "#B5B5B5"

        # 3. 结合哈希结果生成索引（保证连续8个不同，覆盖200个索引）
        num_h = num_hash(self.value) % 200  # 数字哈希映射到0-199
        rank_h = rank_hash(self.rank)
        # 用质数3作为系数，避免哈希碰撞，确保分布均匀
        index = (num_h + rank_h * 3) % 200

        # colors = ['#FFFAFA', '#BBFFFF', '#F8F8FF', '#AEEEEE', '#F5F5F5', '#96CDCD', '#DCDCDC', '#668B8B', '#FFFAF0', '#98F5FF', '#FDF5E6', '#8EE5EE', '#FAF0E6', '#7AC5CD', '#FAEBD7', '#53868B', '#FFEFD5', '#00F5FF', '#FFEBCD', '#00E5EE', '#FFE4C4', '#00C5CD', '#FFDAB9', '#00868B', '#FFDEAD', '#00FFFF', '#FFE4B5', '#00EEEE', '#FFF8DC', '#00CDCD', '#FFFFF0', '#008B8B', '#FFFACD', '#97FFFF', '#FFF5EE', '#8DEEEE', '#F0FFF0', '#79CDCD', '#F5FFFA', '#528B8B', '#F0FFFF', '#7FFFD4', '#F0F8FF', '#76EEC6', '#E6E6FA', '#66CDAA', '#FFF0F5', '#458B74', '#FFE4E1', '#C1FFC1', '#FFFFFF', '#B4EEB4', '#000000', '#9BCD9B', '#2F4F4F', '#698B69', '#696969', '#54FF9F', '#708090', '#4EEE94', '#778899', '#43CD80', '#BEBEBE', '#2E8B57', '#D3D3D3', '#9AFF9A', '#191970', '#90EE90', '#000080', '#7CCD7C', '#6495ED', '#548B54', '#483D8B', '#00FF7F', '#6A5ACD', '#00EE76', '#7B68EE', '#00CD66', '#8470FF', '#008B45', '#0000CD', '#00FF00', '#4169E1', '#00EE00', '#0000FF', '#00CD00', '#1E90FF', '#008B00', '#00BFFF', '#7FFF00', '#87CEEB', '#76EE00', '#87CEFA', '#66CD00', '#4682B4', '#458B00', '#B0C4DE', '#C0FF3E', '#ADD8E6', '#B3EE3A', '#B0E0E6', '#9ACD32', '#AFEEEE', '#698B22', '#00CED1', '#CAFF70', '#48D1CC', '#BCEE68', '#40E0D0', '#A2CD5A', '#00FFFF', '#6E8B3D', '#E0FFFF', '#FFF68F', '#5F9EA0', '#EEE685', '#66CDAA', '#CDC673', '#7FFFD4', '#8B864E', '#006400', '#FFEC8B', '#556B2F', '#EEDC82', '#8FBC8F', '#CDBE70', '#2E8B57', '#8B814C', '#3CB371', '#FFFFE0', '#20B2AA', '#EEEED1', '#98FB98', '#CDCDB4', '#00FF7F', '#8B8B7A', '#7CFC00', '#FFFF00', '#00FF00', '#EEEE00', '#7FFF00', '#CDCD00', '#00FA9A', '#8B8B00', '#ADFF2F', '#FFD700', '#32CD32', '#EEC900', '#9ACD32', '#CDAD00', '#228B22', '#8B7500', '#6B8E23', '#FFC125', '#BDB76B', '#EEB422', '#EEE8AA', '#CD9B1D', '#FAFAD2', '#8B6914', '#FFFFE0', '#FFB90F', '#FFFF00', '#EEAD0E', '#FFD700', '#CD950C', '#EEDD82', '#8B658B', '#DAA520', '#FFC1C1', '#B8860B', '#EEB4B4', '#BC8F8F', '#CD9B9B', '#CD5C5C', '#8B6969', '#8B4513', '#FF6A6A', '#A0522D', '#EE6363', '#CD853F', '#CD5555', '#DEB887', '#8B3A3A', '#F5F5DC', '#FF8247', '#F5DEB3', '#EE7942', '#F4A460', '#CD6839', '#D2B48C', '#8B4726', '#D2691E', '#FFD39B', '#B22222', '#EEC591', '#A52A2A', '#CDAA7D', '#E9967A', '#8B7355', '#FA8072', '#FFE7BA', '#FFA07A', '#EED8AE', '#FFA500', '#CDBA96', '#FF8C00', '#8B7E66', '#FF7F50', '#FFA54F', '#F08080', '#EE9A49', '#FF6347', '#CD853F', '#FF4500', '#8B5A2B', '#FF0000', '#FF7F24', '#FF69B4', '#EE7621', '#FF1493', '#CD661D', '#FFC0CB', '#8B4513', '#FFB6C1', '#FF3030', '#DB7093', '#EE2C2C', '#B03060', '#CD2626', '#C71585', '#8B1A1A', '#D02090', '#FF4040', '#FF00FF', '#EE3B3B', '#EE82EE', '#CD3333', '#DDA0DD', '#8B2323', '#DA70D6', '#FF8C69', '#BA55D3', '#EE8262', '#9932CC', '#CD7054', '#9400D3', '#8B4C39', '#8A2BE2', '#FFA07A', '#A020F0', '#EE9572', '#9370DB', '#CD8162', '#D8BFD8', '#8B5742', '#FFFAFA', '#FFA500', '#EEE9E9', '#EE9A00', '#CDC9C9', '#CD8500', '#8B8989', '#8B5A00', '#FFF5EE', '#FF7F00', '#EEE5DE', '#EE7600', '#CDC5BF', '#CD6600', '#8B8682', '#8B4500', '#FFEFDB', '#FF7256', '#EEDFCC', '#EE6A50', '#CDC0B0', '#CD5B45', '#8B8378', '#8B3E2F', '#FFE4C4', '#FF6347', '#EED5B7', '#EE5C42', '#CDB79E', '#CD4F39', '#8B7D6B', '#8B3626', '#FFDAB9', '#FF4500', '#EECBAD', '#EE4000', '#CDAF95', '#CD3700', '#8B7765', '#8B2500', '#FFDEAD', '#FF0000', '#EECFA1', '#EE0000', '#CDB38B', '#CD0000', '#8B795E', '#8B0000', '#FFFACD', '#FF1493', '#EEE9BF', '#EE1289', '#CDC9A5', '#CD1076', '#8B8970', '#8B0A50', '#FFF8DC', '#FF6EB4', '#EEE8CD', '#EE6AA7', '#CDC8B1', '#CD6090', '#8B8878', '#8B3A62', '#FFFFF0', '#FFB5C5', '#EEEEE0', '#EEA9B8', '#CDCDC1', '#CD919E', '#8B8B83', '#8B636C', '#F0FFF0', '#FFAEB9', '#E0EEE0', '#EEA2AD', '#C1CDC1', '#CD8C95', '#838B83', '#8B5F65', '#FFF0F5', '#FF82AB', '#EEE0E5', '#EE799F', '#CDC1C5', '#CD6889', '#8B8386', '#8B475D', '#FFE4E1', '#FF34B3', '#EED5D2', '#EE30A7', '#CDB7B5', '#CD2990', '#8B7D7B', '#8B1C62', '#F0FFFF', '#FF3E96', '#E0EEEE', '#EE3A8C', '#C1CDCD', '#CD3278', '#838B8B', '#8B2252', '#836FFF', '#FF00FF', '#7A67EE', '#EE00EE', '#6959CD', '#CD00CD', '#473C8B', '#8B008B', '#4876FF', '#FF83FA', '#436EEE', '#EE7AE9', '#3A5FCD', '#CD69C9', '#27408B', '#8B4789', '#0000FF', '#FFBBFF', '#0000EE', '#EEAEEE', '#0000CD', '#CD96CD', '#00008B', '#8B668B', '#1E90FF', '#E066FF', '#1C86EE', '#D15FEE', '#1874CD', '#B452CD', '#104E8B', '#7A378B', '#63B8FF', '#BF3EFF', '#5CACEE', '#B23AEE', '#4F94CD', '#9A32CD', '#36648B', '#68228B', '#00BFFF', '#9B30FF', '#00B2EE', '#912CEE', '#009ACD', '#7D26CD', '#00688B', '#551A8B', '#87CEFF', '#AB82FF', '#7EC0EE', '#9F79EE', '#6CA6CD', '#8968CD', '#4A708B', '#5D478B', '#B0E2FF', '#FFE1FF', '#A4D3EE', '#EED2EE', '#8DB6CD', '#CDB5CD', '#607B8B', '#8B7B8B', '#C6E2FF', '#1C1C1C', '#B9D3EE', '#363636', '#9FB6CD', '#4F4F4F', '#6C7B8B', '#696969', '#CAE1FF', '#828282', '#BCD2EE', '#9C9C9C', '#A2B5CD', '#B5B5B5', '#6E7B8B', '#CFCFCF', '#BFEFFF', '#E8E8E8', '#B2DFEE', '#A9A9A9', '#9AC0CD', '#00008B', '#68838B', '#008B8B', '#E0FFFF', '#8B008B', '#D1EEEE', '#8B0000', '#B4CDCD', '#7A8B8B', '#90EE90']
        colors = ['#8B8B00', '#8A2BE2', '#4169E1', '#FFB90F', '#FFA500', '#BA55D3', '#90EE90', '#87CEEB', '#3A5FCD', '#FF4500', '#8B4500', '#EEB422', '#548B54', '#CD5555', '#CDCD00', '#8B1A1A', '#00CD66', '#FF1493', '#528B8B', '#698B69', '#CD3333', '#DB7093', '#473C8B', '#CD8500', '#7CCD7C', '#FF7F50', '#4F94CD', '#009ACD', '#FFC0CB', '#B452CD', '#104E8B', '#CD3700', '#9BCD9B', '#1E90FF', '#FFA07A', '#FF7F00', '#AFEEEE', '#4876FF', '#6A5ACD', '#00EEEE', '#7A378B', '#CD4F39', '#00868B', '#CD96CD', '#8DEEEE', '#FF00FF', '#CD6600', '#B0E0E6', '#C71585', '#EE7600', '#8B3626', '#00FFFF', '#E9967A', '#36648B', '#D02090', '#9370DB', '#8B658B', '#54FF9F', '#2E8B57', '#FF00FF', '#EEB4B4', '#483D8B', '#FF6A6A', '#00FF00', '#ADD8E6', '#8B7500', '#00CDCD', '#EE6363', '#EE0000', '#CD950C', '#E066FF', '#FF0000', '#7A67EE', '#FF6347', '#FF8C69', '#8B4C39', '#8470FF', '#7B68EE', '#8B3E2F', '#0000FF', '#D15FEE', '#27408B', '#76EE00', '#EEC900', '#CD8162', '#B0C4DE', '#EE9A00', '#4682B4', '#FF8C00', '#FFA500', '#EE2C2C', '#00C5CD', '#B4EEB4', '#00008B', '#CD2626', '#008B45', '#7D26CD', '#6959CD', '#DB7093', '#D02090', '#0000CD', '#BF3EFF', '#48D1CC', '#00FF7F', '#8B6914', '#CD9B9B', '#FF6347', '#B03060', '#8B4789', '#76EEC6', '#DA70D6', '#FFC1C1', '#CDAD00', '#EE4000', '#436EEE', '#43CD80', '#00EE76', '#1874CD', '#00FFFF', '#FFB6C1', '#0000FF', '#00B2EE', '#EE9572', '#FFA07A', '#EEAEEE', '#FFD700', '#00CED1', '#6495ED', '#68228B', '#836FFF', '#FA8072', '#C71585', '#C1FFC1', '#7FFF00', '#9400D3', '#00CD00', '#D2691E', '#EE8262', '#008B00', '#CD0000', '#40E0D0', '#8B2323', '#F08080', '#4EEE94', '#CD661D', '#8B3A3A', '#FF7256', '#912CEE', '#66CDAA', '#8B5742', '#8B6969', '#1E90FF', '#CD8500', '#00BFFF', '#B23AEE', '#00F5FF', '#EE3B3B', '#8B668B', '#8B2500', '#CD7054', '#9B30FF', '#97FFFF', '#CD9B1D', '#00BFFF', '#00EE00', '#7FFFD4', '#EE6A50', '#EEAD0E', '#FFBBFF', '#FFA500', '#EEEE00', '#008B8B', '#79CDCD', '#FF0000', '#87CEFA', '#FF4040', '#1C86EE', '#EE7621', '#B03060', '#63B8FF', '#FFC125', '#EE82EE', '#0000EE', '#8B4513', '#FF3030', '#8B5A00', '#EE9A00', '#DDA0DD', '#FF4500', '#9AFF9A', '#CD5B45', '#FF69B4', '#00E5EE', '#0000CD', '#EE5C42', '#9A32CD', '#5CACEE', '#A020F0', '#A52A2A', '#9932CC', '#B22222']
        return colors[index]


class DataAlgorithm:
    def __init__(self):
        pass

    def translateStrToData(self, string):
        split_index = 0
        while split_index < len(string) and string[split_index].isdigit():
            split_index += 1

        # 分割数字和字母部分
        num_str = string[:split_index]  # 数字部分（字符串）
        alpha_str = string[split_index:]  # 字母部分（字符串）

        # 转换数字部分为int类型
        if num_str == "":
            return Data(-1, alpha_str)
        return Data(int(num_str), alpha_str)

    def getDataRange(self, gameSave):
        '''
        反正就是最大的值，从它往前10个是场上的范围，生成的范围是前5个
        1、2、4、8、16、32、64、128、256、512、1024，场上最大是1024的时候，只生成32及以前的
        :param gameSave:
        :return:
        '''
        pass




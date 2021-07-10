import abc

class source:

    @abc.abstractmethod
    def write_summary_sentence_and_index(self,topic_no,res_sentence_index):
        pass

    @abc.abstractmethod
    def check_res_folder_exist(self):
        pass

    @abc.abstractmethod
    def get_all_ori_sentence(self, topic_no):
        pass

    @abc.abstractmethod
    def get_all_dst_sentence(self, topic_no):
        pass

    @abc.abstractmethod
    def write_summary_sentences(self, topic_no, summary_sentences):
        pass

    @abc.abstractmethod
    def write_summary_sentences_index(self, topic_no, res_sentence_index):
        pass

    @abc.abstractmethod
    def write_parameters(self, obj):
        pass

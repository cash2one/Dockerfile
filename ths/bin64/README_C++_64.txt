1. �������ǻ��� centos6.5 64λ�汾�����1.0�汾, �ṩ��̬�����, �������������ο�test����

2. ��ʹ��ǰ������� ldd libShellExport.so, ldd hqdatafeed�� ldd libFTDataInterface.so �鿴�������Ļ����Ƿ��Ѿ���ȫ, �������ȫ,��ʹ��yum����apt-get��װ

yum install -y libgcc.i686 

3. �ڱ���ʹ��ǰ,����ӵ�ǰĿ¼��ϵͳ�������� LD_LIBRARY_PATH; ���ڱ�����ʹ�õ��������ļ�,�����Ƶ�ϵͳĿ¼,����ᵼ�������쳣,
�����ǰĿ¼�� /root/Linux/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Linux/bin

ע��:
	(1) ���ʹ�ö�̬���صķ�ʽ����, �����ڳ������ʱ��� -lpthread ���������
		�첽�ӿڻ���ʵʱ�ӿڶ��̱߳���
	(2) ���ö�̬���¼�ɹ�����е��� hqdatafeed ���̵�������,�����������ʵʱ��������
		����32λ��������,�Լ��ݵķ�ʽ��64λ����������, ����kill
	
	
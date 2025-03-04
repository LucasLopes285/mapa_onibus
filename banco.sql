PGDMP                         }            mapa_onibus %   14.13 (Ubuntu 14.13-0ubuntu0.22.04.1) %   14.13 (Ubuntu 14.13-0ubuntu0.22.04.1) 2    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    25165    mapa_onibus    DATABASE     `   CREATE DATABASE mapa_onibus WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'pt_BR.UTF-8';
    DROP DATABASE mapa_onibus;
                postgres    false            �           0    0    DATABASE mapa_onibus    ACL     -   GRANT ALL ON DATABASE mapa_onibus TO lukita;
                   postgres    false    4291                        3079    25166    postgis 	   EXTENSION     ;   CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
    DROP EXTENSION postgis;
                   false            �           0    0    EXTENSION postgis    COMMENT     ^   COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';
                        false    2            �            1259    26238    onibus    TABLE     �   CREATE TABLE public.onibus (
    id integer NOT NULL,
    nome character varying(30) NOT NULL,
    rota_id integer,
    paradas integer[] NOT NULL
);
    DROP TABLE public.onibus;
       public         heap    postgres    false            �           0    0    TABLE onibus    ACL     /   GRANT SELECT ON TABLE public.onibus TO lukita;
          public          postgres    false    222            �            1259    26237    onibus_id_seq    SEQUENCE     �   CREATE SEQUENCE public.onibus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.onibus_id_seq;
       public          postgres    false    222            �           0    0    onibus_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.onibus_id_seq OWNED BY public.onibus.id;
          public          postgres    false    221            �           0    0    SEQUENCE onibus_id_seq    ACL     ?   GRANT SELECT,USAGE ON SEQUENCE public.onibus_id_seq TO lukita;
          public          postgres    false    221            �            1259    26263    onibus_paradas    TABLE     g   CREATE TABLE public.onibus_paradas (
    onibus_id integer NOT NULL,
    parada_id integer NOT NULL
);
 "   DROP TABLE public.onibus_paradas;
       public         heap    postgres    false            �           0    0    TABLE onibus_paradas    ACL     7   GRANT SELECT ON TABLE public.onibus_paradas TO lukita;
          public          postgres    false    223            �            1259    26216    paradas    TABLE     �   CREATE TABLE public.paradas (
    id integer NOT NULL,
    nome character varying NOT NULL,
    coordenadas json NOT NULL,
    descricao character varying
);
    DROP TABLE public.paradas;
       public         heap    lukita    false            �            1259    26215    paradas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.paradas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.paradas_id_seq;
       public          lukita    false    218            �           0    0    paradas_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.paradas_id_seq OWNED BY public.paradas.id;
          public          lukita    false    217            �            1259    26206    rotas    TABLE     v   CREATE TABLE public.rotas (
    id integer NOT NULL,
    nome character varying NOT NULL,
    pontos json NOT NULL
);
    DROP TABLE public.rotas;
       public         heap    lukita    false            �            1259    26205    rotas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rotas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.rotas_id_seq;
       public          lukita    false    216            �           0    0    rotas_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.rotas_id_seq OWNED BY public.rotas.id;
          public          lukita    false    215            �            1259    26226    usuarios    TABLE     �   CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nome character varying NOT NULL,
    email character varying NOT NULL,
    senha character varying NOT NULL,
    tipo character varying NOT NULL
);
    DROP TABLE public.usuarios;
       public         heap    lukita    false            �            1259    26225    usuarios_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usuarios_id_seq;
       public          lukita    false    220            �           0    0    usuarios_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;
          public          lukita    false    219                       2604    26241 	   onibus id    DEFAULT     f   ALTER TABLE ONLY public.onibus ALTER COLUMN id SET DEFAULT nextval('public.onibus_id_seq'::regclass);
 8   ALTER TABLE public.onibus ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221    222                       2604    26219 
   paradas id    DEFAULT     h   ALTER TABLE ONLY public.paradas ALTER COLUMN id SET DEFAULT nextval('public.paradas_id_seq'::regclass);
 9   ALTER TABLE public.paradas ALTER COLUMN id DROP DEFAULT;
       public          lukita    false    217    218    218                       2604    26209    rotas id    DEFAULT     d   ALTER TABLE ONLY public.rotas ALTER COLUMN id SET DEFAULT nextval('public.rotas_id_seq'::regclass);
 7   ALTER TABLE public.rotas ALTER COLUMN id DROP DEFAULT;
       public          lukita    false    215    216    216                       2604    26229    usuarios id    DEFAULT     j   ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);
 :   ALTER TABLE public.usuarios ALTER COLUMN id DROP DEFAULT;
       public          lukita    false    220    219    220            �          0    26238    onibus 
   TABLE DATA           <   COPY public.onibus (id, nome, rota_id, paradas) FROM stdin;
    public          postgres    false    222   f3       �          0    26263    onibus_paradas 
   TABLE DATA           >   COPY public.onibus_paradas (onibus_id, parada_id) FROM stdin;
    public          postgres    false    223   �3       �          0    26216    paradas 
   TABLE DATA           C   COPY public.paradas (id, nome, coordenadas, descricao) FROM stdin;
    public          lukita    false    218   �3       �          0    26206    rotas 
   TABLE DATA           1   COPY public.rotas (id, nome, pontos) FROM stdin;
    public          lukita    false    216   4       	          0    25476    spatial_ref_sys 
   TABLE DATA           X   COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
    public          postgres    false    211   g4       �          0    26226    usuarios 
   TABLE DATA           @   COPY public.usuarios (id, nome, email, senha, tipo) FROM stdin;
    public          lukita    false    220   �4       �           0    0    onibus_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.onibus_id_seq', 1, false);
          public          postgres    false    221            �           0    0    paradas_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.paradas_id_seq', 3, true);
          public          lukita    false    217            �           0    0    rotas_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.rotas_id_seq', 2, true);
          public          lukita    false    215            �           0    0    usuarios_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.usuarios_id_seq', 4, true);
          public          lukita    false    219                       2606    26247    onibus onibus_nome_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.onibus
    ADD CONSTRAINT onibus_nome_key UNIQUE (nome);
 @   ALTER TABLE ONLY public.onibus DROP CONSTRAINT onibus_nome_key;
       public            postgres    false    222            !           2606    26267 "   onibus_paradas onibus_paradas_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.onibus_paradas
    ADD CONSTRAINT onibus_paradas_pkey PRIMARY KEY (onibus_id, parada_id);
 L   ALTER TABLE ONLY public.onibus_paradas DROP CONSTRAINT onibus_paradas_pkey;
       public            postgres    false    223    223                       2606    26245    onibus onibus_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.onibus
    ADD CONSTRAINT onibus_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.onibus DROP CONSTRAINT onibus_pkey;
       public            postgres    false    222                       2606    26223    paradas paradas_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.paradas
    ADD CONSTRAINT paradas_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.paradas DROP CONSTRAINT paradas_pkey;
       public            lukita    false    218                       2606    26213    rotas rotas_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.rotas
    ADD CONSTRAINT rotas_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.rotas DROP CONSTRAINT rotas_pkey;
       public            lukita    false    216                       2606    26235    usuarios usuarios_email_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);
 E   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_email_key;
       public            lukita    false    220                       2606    26233    usuarios usuarios_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            lukita    false    220                       1259    26224    ix_paradas_id    INDEX     ?   CREATE INDEX ix_paradas_id ON public.paradas USING btree (id);
 !   DROP INDEX public.ix_paradas_id;
       public            lukita    false    218                       1259    26214    ix_rotas_id    INDEX     ;   CREATE INDEX ix_rotas_id ON public.rotas USING btree (id);
    DROP INDEX public.ix_rotas_id;
       public            lukita    false    216                       1259    26236    ix_usuarios_id    INDEX     A   CREATE INDEX ix_usuarios_id ON public.usuarios USING btree (id);
 "   DROP INDEX public.ix_usuarios_id;
       public            lukita    false    220            #           2606    26268 ,   onibus_paradas onibus_paradas_onibus_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.onibus_paradas
    ADD CONSTRAINT onibus_paradas_onibus_id_fkey FOREIGN KEY (onibus_id) REFERENCES public.onibus(id) ON DELETE CASCADE;
 V   ALTER TABLE ONLY public.onibus_paradas DROP CONSTRAINT onibus_paradas_onibus_id_fkey;
       public          postgres    false    223    4127    222            $           2606    26273 ,   onibus_paradas onibus_paradas_parada_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.onibus_paradas
    ADD CONSTRAINT onibus_paradas_parada_id_fkey FOREIGN KEY (parada_id) REFERENCES public.paradas(id) ON DELETE CASCADE;
 V   ALTER TABLE ONLY public.onibus_paradas DROP CONSTRAINT onibus_paradas_parada_id_fkey;
       public          postgres    false    218    223    4118            "           2606    26248    onibus onibus_rota_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.onibus
    ADD CONSTRAINT onibus_rota_id_fkey FOREIGN KEY (rota_id) REFERENCES public.rotas(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.onibus DROP CONSTRAINT onibus_rota_id_fkey;
       public          postgres    false    4115    216    222            �      x������ � �      �      x������ � �      �   ^   x�3�H,JLIT(J<�<Q!���|��Ԥ��L ��Z)'�D�JA�H���BGA)'/�55�3��(:��"37_!Q� �?95��(1�+F��� ��6      �   I   x�3��/ITpN�+)�献V�I,Q�R�5�31��QP��KqMM��,-ku���ț��rQټ=... ��)j      	      x������ � �      �   �   x�e�MO�0 ���Wx�\BenN`@8�HF�t��"��|l���ŋq�7y�&�c�x����b��ᠻ�s�0�`���Q7���(��Xzkh���ɥ�a��@)�!�P���JB�+U�VL��8	L�������>��Q8�dJY[:�@}��$�����ɯ�kS�e�B=�-��pT��G�`A1`��Oxa��K���y'�Ψ0^��Ǝ8/��������wv�h?�j�q��q�j���5g�     